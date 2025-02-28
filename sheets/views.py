from django.shortcuts import render, redirect, get_object_or_404
from .models import Spreadsheet, Cell, Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import string
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SpreadsheetSerializer, CellSerializer 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SpreadsheetSerializer, CellSerializer

# Dashboard View (Shows all spreadsheets for the logged-in user)
from django.utils.timezone import now

def some_view(request):
    return render(request, "your_template.html", {"timestamp": int(now().timestamp())})
@login_required
def dashboard_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    spreadsheets = Spreadsheet.objects.filter(profile=profile)  # ✅ Only user-specific sheets
    return render(request, 'sheets/dashboard.html', {'spreadsheets': spreadsheets})
@login_required
def delete_spreadsheet(request, sheet_id):
    """Delete a spreadsheet if it belongs to the logged-in user."""
    profile = get_object_or_404(Profile, user=request.user)
    spreadsheet = get_object_or_404(Spreadsheet, id=sheet_id, profile=profile)

    spreadsheet.delete()
    return JsonResponse({"message": "Spreadsheet deleted successfully!"})


# Create a New Spreadsheet
@login_required
def create_spreadsheet(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure profile exists
    new_sheet = Spreadsheet.objects.create(profile=profile, name="Untitled Spreadsheet")
    return redirect(f'/sheets/{new_sheet.id}/')

# Load Spreadsheet View@login_required
@login_required
def spreadsheet_view(request, sheet_id):
    profile = get_object_or_404(Profile, user=request.user)
    spreadsheet = get_object_or_404(Spreadsheet, id=sheet_id, profile=profile)  # ✅ Restricts access
    cells = Cell.objects.filter(spreadsheet=spreadsheet)

    rows = list(range(1, 11))  # Default: 10 rows
    cols = list(range(1, 6))   # Default: 5 columns
    col_labels = [string.ascii_uppercase[i] for i in range(len(cols))]  # Convert to A, B, C, ...

    saved_cells = {f"cell-{cell.row}-{cell.col}": cell.value for cell in cells}

    return render(request, 'sheets/spreadsheet.html', {
        'spreadsheet': spreadsheet,
        'cells': cells,
        'rows': rows,
        'cols': cols,
        'col_labels': col_labels,
        'saved_cells': json.dumps(saved_cells),  # ✅ Embed saved data in template
    })


# Update Cell Data (AJAX Call from Frontend)
@csrf_exempt
@login_required
def update_cell(request):
    if request.method == "POST":
        data = json.loads(request.body)
        sheet_id = data.get("spreadsheet_id")
        row = int(data.get("row"))
        col = int(data.get("col"))
        value = data.get("value", "")

        profile = get_object_or_404(Profile, user=request.user)
        spreadsheet = get_object_or_404(Spreadsheet, id=sheet_id, profile=profile)

        cell, created = Cell.objects.get_or_create(spreadsheet=spreadsheet, row=row, col=col)
        cell.value = value
        cell.save()

        return JsonResponse({"status": "success", "value": value})
    
    return JsonResponse({"status": "error"})

# Save Spreadsheet Data
@csrf_exempt
@login_required
def save_spreadsheet(request, sheet_id):
    if request.method == "POST":
        data = json.loads(request.body)

        if not data.get("cells"):
            return JsonResponse({"error": "No data received"}, status=400)

        profile = get_object_or_404(Profile, user=request.user)
        spreadsheet = get_object_or_404(Spreadsheet, id=sheet_id, profile=profile)

        # ✅ Update the sheet name if provided
        spreadsheet.name = data.get("name", spreadsheet.name)
        spreadsheet.save()

        # Clear old cell data before saving new data
        Cell.objects.filter(spreadsheet=spreadsheet).delete()

        for cell in data["cells"]:
            row, col = map(int, cell["id"].split("-")[1:])
            Cell.objects.create(spreadsheet=spreadsheet, row=row, col=col, value=cell["value"])

        return JsonResponse({"message": "Spreadsheet saved successfully!"})


# Load Spreadsheet Data (Auto-load when user opens sheet)
@login_required
def load_spreadsheet(request, sheet_id):
    profile = get_object_or_404(Profile, user=request.user)
    spreadsheet = get_object_or_404(Spreadsheet, id=sheet_id, profile=profile)
    cells = Cell.objects.filter(spreadsheet=spreadsheet)

    cell_data = [{"id": f"cell-{cell.row}-{cell.col}", "value": cell.value or ""} for cell in cells]

    return JsonResponse({"cells": cell_data})




# ✅ API to Retrieve All User Sheets
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sheets(request):
    profile = get_object_or_404(Profile, user=request.user)
    sheets = Spreadsheet.objects.filter(profile=profile)  # ✅ Fetch user-specific sheets
    serializer = SpreadsheetSerializer(sheets, many=True)
    return Response(serializer.data)

# ✅ API to Save Sheet Data
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_sheet_data(request):
    try:
        data = request.data  # ✅ DRF automatically handles JSON parsing
        print("🔍 Received Data:", data)  # ✅ Debugging

        if "cells" not in data:
            return Response({"error": "Missing 'cells' key in request."}, status=400)

        profile = get_object_or_404(Profile, user=request.user)

        # ✅ Check if spreadsheet exists for user
        spreadsheet, created = Spreadsheet.objects.get_or_create(
            id=data.get("sheet_id"),
            defaults={'profile': profile, 'name': data.get("name", "Untitled Spreadsheet")}
        )

        # ✅ Remove existing cells before saving new ones
        spreadsheet.cell_set.all().delete()

        # ✅ Save new cell data
        for cell in data["cells"]:
            if "row" not in cell or "col" not in cell or "value" not in cell:
                return Response({"error": "Invalid cell format."}, status=400)
            
            Cell.objects.create(spreadsheet=spreadsheet, row=cell["row"], col=cell["col"], value=cell["value"])

        return Response({"message": "Spreadsheet saved successfully!"})
    
    except Exception as e:
        print("❌ Server Error:", str(e))  # ✅ Debugging
        return Response({"error": "Internal Server Error", "details": str(e)}, status=500)

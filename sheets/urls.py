from django.urls import path
from .views import dashboard_view, spreadsheet_view, create_spreadsheet, save_spreadsheet, load_spreadsheet, delete_spreadsheet
from .views import get_sheets, save_sheet_data 
urlpatterns = [
    path('', dashboard_view, name='dashboard'),  # Landing page
    path('create/', create_spreadsheet, name='create_spreadsheet'),  # New sheet
    path('<int:sheet_id>/', spreadsheet_view, name='spreadsheet'),  # Open sheet
    path("save/", save_spreadsheet, name="save_spreadsheet"),
    path("load/<int:sheet_id>/", load_spreadsheet, name="load_spreadsheet"),
     # ✅ API Routes
    path("api/sheets/", get_sheets, name="get_sheets"),
    path("api/save-sheet/", save_sheet_data, name="save_sheet_data"),
    path("delete/<int:sheet_id>/", delete_spreadsheet, name="delete_spreadsheet"),

]


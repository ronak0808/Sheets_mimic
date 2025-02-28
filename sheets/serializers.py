from rest_framework import serializers
from .models import Spreadsheet, Cell

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ['row', 'col', 'value']

class SpreadsheetSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)

    class Meta:
        model = Spreadsheet
        fields = ['id', 'name', 'created_at', 'cells']

function doGet(e) {

	var params = e.parameter;

	var SpreadSheet = SpreadsheetApp.openById("YOUR_SPREADSHEET_URL");
	var Sheet = SpreadSheet.getSheets()[0];
	var LastRow = Sheet.getLastRow();

	Sheet.getRange(LastRow+1, 1).setValue(params.name);
	Sheet.getRange(LastRow+1, 2).setValue(params.mail);
	Sheet.getRange(LastRow+1, 3).setValue(params.formid);

	var questionCount = Object.keys(params).filter(key => key.startsWith('q')).length;

	for (var i = 1; i <= questionCount; i++) {
		Sheet.getRange(LastRow + 1, 3 + i).setValue(params["q" + i.toString()]);
	}

	return ContentService.createTextOutput(params.thank);
}

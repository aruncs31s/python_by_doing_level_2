# Get data from http://localhost:5000/calc/5/+10
$response = Invoke-RestMethod -Uri "http://localhost:5000/is_complete" -Method Get
# check the response and if the result = "True" , then output "Test Passed"
if ($response.result -eq "True") {
    "^_^ Test Passed"
}
else {
    "X_X Test Failed"
}

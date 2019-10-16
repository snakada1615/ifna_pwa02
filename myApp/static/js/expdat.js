var fs = WScript.CreateObject("Scripting.FileSystemObject");
var file = fs.CreateTextFile("c:\text.txt");
file.Write("マルペケつくろ～");
file.Close();

<p>Search for {{keywords}}</p>
<table id = "results"><tr> <th>Word</th> <th>Count</th></tr>
%for keyword in results:
	<tr><td>{{keyword}}</td><td>{{results[keyword]}}</td></tr>
%end
</table>
<p>Searchhistory</p>
<table id = "history"><tr> <th>Word</th> <th>Count</th></tr>
%for keyword2,value in history:
	<tr><td>{{keyword2}}</td><td>{{value}}</td></tr>
%end
</table>
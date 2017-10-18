<style>
	table {
	    border-collapse: collapse;
	    width: 30%;
	}

	th, td {
	    padding: 8px;
	    text-align: left;
	    border-bottom: 1px solid #ddd;
	}
</style>
<p style="font-family:verdana;font-size:120%; background-color: lightblue;">Search for {{keywords}}</p>
<table id = "results"><tr> <th>Word</th> <th>Count</th></tr>
%for keyword in results:
	<tr><td>{{keyword}}</td><td>{{results[keyword]}}</td></tr>
%end
</table>


%if login: 
<p style=" font-family:verdana;font-size:120%; background-color: lightblue;">Searchhistory</p>
<table id = "history"><tr> <th>Word</th> <th>Count</th></tr>
%for keyword2,value in history:
	<tr><td>{{keyword2}}</td><td>{{value}}</td></tr>
%end
</table>
<p style="font-family:verdana;font-size:120%; background-color: lightblue;">User Recent Search</p>
<table id = "RecentSearch"><tr> <th>Word</th>
%for keyword3 in recentsearch:
	<tr><td>{{keyword3}}</td>
%end
</table>

<p style="float: right;">{{user_email}}</p>
<form action= "/logout" method = "GET"> </br></br>
		
		<input type="submit" value="logout" style="float: right;">
</form>



%else: 
<form action= "/login" method = "GET">
		<input type="submit" value="login" style="float: right;">
</form>
		
%end 

<form action= "/" method = "GET">
			
			<input type="text" name="keywords" style = "width: 300px; height: 30px;">
			<input type="submit" value="Search"></br></br>
<form>






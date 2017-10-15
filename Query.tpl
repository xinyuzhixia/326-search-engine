<html>
<head>
	<style>
	body {
    background-color: lightblue;
		}
	h1 {

		color: white;
		text-align: center;
		font-size:60px;
	}
	form{

		margin:0 auto;
		width:300px;
	}
	</style>
	<title>Googing Search</title>
</head>
	<body>
		<h1>Googing</h1>
			<form action= "/" method = "GET">
			
			<input type="text" name="keywords" style = "width: 300px; height: 30px;"></br></br>
			<input type="submit" value="Search" style="float: right;"></br></br>
			%if Login: 
				<p>{{user_email}}</p>
				<input type="submit" value="logout" style="float: right;" formaction="/logout">
			%else: 
				<input type="submit" value="login" style="float: right;"formaction="/login">
			</form>
	</body>

</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

<html>
<head>
  <title>
    Image search engine
  </title>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  <link rel="stylesheet" type="text/css" href="main.css">
</head>
<body>
  <div class="bigbox">
    <div class="contentbox">
      <h1>Image search engine</h1>
      <p>
      text
      </p>
			<h2>Search</h2>
			<p>
      text
			</p>
      <form action="index.php" method="post">
      Query: <input type="text" name="queryimg">
      <input type="submit">
      </form>
      <h2>Results</h2>
      <?php
      echo "stnrtsisnt";
      ?>
      Query entered: <?php echo $_POST["queryimg"]; ?>
    </div>

    <div class="bottombox">
    Footer.
    </div>
  </div>
</body>
</html>

<?php
$host   = "localhost";
$user   = "your_db_user";
$pass   = "your_db_password";
$dbname = "brooder_system";

$conn = new mysqli($host, $user, $pass, $dbname);
if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}

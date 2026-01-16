<?php

$name = $_POST["name"]
$email = $_POST["email"]
$subject = $_POST["subject"]
$message = $_POST["message"]

require "vendor/autoload.php";

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;

$mail = new PHPMailer(true);

$mail -> isSMTP();
$mail -> SMTPAuth = True;

$mail -> HOST = "smtp.example.com";
$mail -> SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
$mail -> Port = 587;

$mail -> Username = "you@example.com";
$mail -> Password = "password";

$mail -> setFrom($email, $name);
$mail -> addAddress ("dave@example.com");

$mail -> Subject = $subject;
$mail -> Body = $message;

$mail -> Send();

echo "Email sent";





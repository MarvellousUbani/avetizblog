<?php
require("PHPMailerAutoload.php");
function sendMail($address,$username,$body){
            $mail = new PHPMailer();
            $mail->IsSMTP(); // telling the class to use SMTP
            //$mail->Host       = "smtp.gmail.com"; // SMTP server
            $mail->SMTPDebug  = 1;                     // enables SMTP debug information (for testing)
                                // 1 = errors and messages
                                                                           // 2 = messages only
            // $mail->SMTPAuth   = true;                  // enable SMTP authentication
            // $mail->SMTPSecure = "ssl";                 // sets the prefix to the servier
            // $mail->Host       = "smtp.gmail.com";      // sets  as the SMTP server
            // $mail->Port       = 465;                   // set the SMTP port for the server
            // $mail->Username   = "xyz@gmail.com";  // username
            // $mail->Password   = "test121232";            // password

            $mail->SetFrom('contact@example.co.in', 'Contact');

            $mail->Subject    = "Change Password on AvetiZ Career";



            $mail->MsgHTML($body);

            $address = $address;
            $mail->AddAddress($address, $username);
            $mail->AddCC('contact@example.co.in');

            if(!$mail->Send()) {
            echo "Mailer Error: " . $mail->ErrorInfo;
            } else {
            echo "Message sent!";
            }

}
sendMail('abiodun.toluwanii@gmail.com', 'career@avetiz.com','test-mail');
?>

<?php
// Check for empty fields
$error='';
$sucess='';
require_once('../includes/config.php');


require("PHPMailerAutoload.php");

$pwd = bin2hex(openssl_random_pseudo_bytes(4));

if (isset($_POST['submit'])){

$email = strip_tags(htmlspecialchars($_POST['email']));

      


$stmt=$db->prepare('select count(*) from user where email=:email');
$stmt->execute(array(
':email'=> $_POST['email'],
));
$row=$stmt->fetch(PDO::FETCH_NUM);
if (!$row[0]==0){
      
      
//change password in database

$stmt2=$db->prepare('UPDATE user set password=:pwd where email=:email');
$stmt2->execute(array(

':pwd'=>md5($pwd),
':email' =>$_POST['email'],
));

      
      
// Create the email and send the message
$mail = new PHPMailer();

$mail->IsSMTP(); // telling the class to use SMTP 

$mail->Host = "smtp.gmail.com"; // SMTP server

$mail->SMTPAuth = true;

$mail->Username = "myschoolrents@gmail.com";  
               
$mail->Password = "test123321"; 



$mail->SMTPSecure = "tls"; 

$mail->Port = 587;    

$mail->From = "myschoolrents@gmail.com"; 

$mail->FromName = "From Avetiz";

$mail->AddAddress($email);

$mail->addReplyTo($email, "Reply");
 
$mail->isHTML(true);

$mail->Subject = "Password Reset From Avetiz" ; 


$mail->Body = "New Password is  :".$pwd; 

$mail->WordWrap = 50;

if(!$mail->Send()) { 
$error='Message was not sent.'; echo 'Mailer error: ' . $mail->ErrorInfo;
echo 'Message was not sent.'; echo 'Mailer error:' . $mail->ErrorInfo; } 
else {
echo '<p style="color:green">Your new Password has been sent to your email  Please go <a href="../login.php">Login</a> again with your new password</p>';
$sucess='Your new Password has been sent to your email  Please go <a href="../login.php">Login</a> again with your new password';
 }    
}
else{
$error='<p style="color:red">User not found. <a href="../signup.php"><font size="2px"><i> Please Signup</i></font></a></p>';


}

}
      
?>



<!DOCTYPE html>
<html lang="en">
    
<!-- Mirrored from designstream.co.in/templates/html/job-express/login.html by HTTrack Website Copier/3.x [XR&CO'2014], Fri, 09 Jun 2017 13:58:50 GMT -->
<head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Avetiz</title>   
 
        <!-- Bootstrap -->
        <link href="../assets/plugins/bootstrap/css/bootstrap.min.css" rel="stylesheet">
        <!--font awesome-->
        <link href="../assets/plugins/font-awesome/css/font-awesome.min.css" rel="stylesheet">
        <!--custom css-->
        <link href="../assets/plugins/themify/themify-icons.css" rel="stylesheet">
        <link href="../assets/css/style.css" rel="stylesheet">
        <link href="../assets/css/responsive.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,500,500i,700,700i,900,900i" rel="stylesheet">
    </head>
<body>

<div class="container">
    <div class="row">
        <div class="row">
            <div class="col-md-4 col-md-offset-4">
                <div class="panel panel-default">
                    <div class="panel-body">
                        <div class="text-center">
                          <h3><i class="fa fa-lock fa-4x"></i></h3>
                          <h2 class="text-center">Forgot Password?</h2>
                          <p>You can reset your password here.</p>
                            <div class="panel-body">
                              
                              <form class="form" method="post" >
                                <fieldset>
                                  <div class="form-group">
                                    <div class="input-group">
                                      <span class="input-group-addon"><i class="glyphicon glyphicon-envelope color-blue"></i></span>
                                      
                                      <input id="emailInput" name="email" placeholder="email address" class="form-control" type="email" oninvalid="setCustomValidity('Please enter a valid email address!')" onchange="try{setCustomValidity('')}catch(e){}" required="">
                                    </div>
                                  </div>
                                                  <?php echo $sucess ?> 
                                                  <?php echo $error ?> 
                                  <div class="form-group">
                                    <input class="btn btn-lg btn-primary btn-block" value="Send My Password" name="submit" type="submit">
                                  </div>
                                </fieldset>
                              </form>
                              
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</body>

<?php
require_once('includes/config.php');
require_once('mail/mail-test.php');
if(!$user->is_logged_in()){ header('Location: login2.php'); }
$stmt2=$db->prepare('SELECT count(*) FROM job_user WHERE useremail=:id AND jobid=:jobid');
$stmt2->execute(array(
':id'=>$_SESSION['id'],
':jobid'=>$_GET['id'],
));
$row=$stmt2->fetch(PDO::FETCH_NUM);
if (!$row[0]==0){
      $_SESSION['apply_error']= '<strong>Error in Application</strong> You cant apply for the same role twice !';
      header('Location: view-resume.php');
      exit;
}
elseif($row[0]==0){
$a=$_SESSION['id'];
$stmt=$db->prepare('INSERT into job_user (useremail, jobid, status) values(:email, :id, :status)');
$stmt->execute(array(
':email' =>$a,
':id'   =>$_GET['id'],
':status' =>'Applied',
));
$stmt5=$db->prepare('SELECT title FROM  job WHERE id=:id');
$stmt5->execute(array(
':id'=>$_GET['id'],
));
$row5=$stmt5->fetch();
$job=$row5['title'];
echo 'great';
$message='This is to notify you of the application for the position of '.$job .' on AvetiZ Career Website.';
$_SESSION['apply']=true;
a=sendMail('recruitment@avetiz.com', 'career@avetiz.com',$message);
header('Location: view-resume.php');
exit;
}

?>

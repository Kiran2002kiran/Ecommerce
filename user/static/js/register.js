function validateregister(){
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value;
    if(username==""){
        document.getElementById('msg').innerHTML='please enter your name'
        return false
    }
    if(email==""){
        document.getElementById('msg').innerHTML='please enter your email'
        return false
    }
    if(password==""){
        document.getElementById('msg').innerHTML='please enter your password'
        return false
    }
    if(password.length<8){
        document.getElementById('msg').innerHTML='Password must need minimum 8 characters'
        return false
    }
    if(password!=password2){
        document.getElementById('msg').innerHTML='Password do not match'
        return false
    }
    else{
        return true
    }
}
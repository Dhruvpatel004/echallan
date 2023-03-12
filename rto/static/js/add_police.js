let usernameField = document.querySelector("#p_username");
let usernameField_messg = document.querySelector("#username_check");
let submitBtn = document.querySelector("#submitBtn");

console.log("Entered Username : ",usernameField);
usernameField.addEventListener("keyup",(e)=>{
          let usernameValue=e.target.value;
          console.log(usernameValue);
          console.log(usernameValue.length);
          if(usernameValue.length>0)
          {
            fetch("validate-username",{
            body:JSON.stringify({username:usernameValue}),
            method:'POST',
          }
          )
            .then(res=>res.json()).then(data=>
          {
            console.log("fetching data from server by api"),
            console.log("data",data);
            if(data.username_error)
            { usernameField_messg.innerHTML=`${data.username_error}`;
              submitBtn.disabled = true;
            }
            else{
            usernameField_messg.innerHTML=``;
            submitBtn.disabled = false;
            }
          })
          }
});


function showpass() {
  var x = document.getElementById("p_password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
let v_no_Field = document.querySelector("#v_no");
let view_v = document.querySelector("#view_v");

let v_no_Field_messg = document.querySelector("#v_no_check");
let submitBtn = document.querySelector("#submitBtn");

v_no_Field.addEventListener("keyup",(e)=>{
    let Value=e.target.value;
    // console.log(Value);
    // console.log(Value.length);
    if(Value.length>0)
    {
      fetch("validate-vehical-number",{
      body:JSON.stringify({vehical_number:Value}),
      method:'POST',
    }
    )
      .then(res=>res.json()).then(data=>
    {
      // console.log("fetching data from server by api"),
      // console.log("data",data);
      if(data.vehical_number_error)
      { v_no_Field_messg.innerHTML=`${data.vehical_number_error}`;
        view_v.style.display = "none";
        submitBtn.disabled = true;
      }
      else{
      v_no_Field_messg.innerHTML=``;
      view_v.style.display = "block";
      view_v.href=Value;

      submitBtn.disabled = false;
      }
    })
    }
    else{
      view_v.style.display = "none";
    }
});


function myFunction() {
    let b = document.querySelector("#b");
    let s = document.querySelector("#s");

    b.style.display = "none";
    s.style.display = "block";
    
  }
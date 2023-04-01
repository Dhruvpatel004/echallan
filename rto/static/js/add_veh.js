let v_no_Field = document.querySelector("#v_no");
let v_eng_no_Field = document.querySelector("#v_eng_no");
let v_chass_no_Field = document.querySelector("#v_chass_no");

let v_no_Field_messg = document.querySelector("#v_no_check");
let v_eng_no_Field_messg = document.querySelector("#v_eng_no_check");
let v_chass_no_Field_messg = document.querySelector("#v_chass_no_check");

let submitBtn = document.querySelector("#submitBtn");

console.log("Entered Vehical No : ",v_chass_no_Field);
v_no_Field.addEventListener("keyup",(e)=>{
          let Value=e.target.value;
          console.log(Value);
          console.log(Value.length);
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
              submitBtn.disabled = true;
            }
            else{
            v_no_Field_messg.innerHTML=``;
            submitBtn.disabled = false;
            }
          })
          }
});


v_eng_no_Field.addEventListener("keyup",(e)=>{
    let Value=e.target.value;
    console.log(Value);
    console.log(Value.length);
    if(Value.length>0)
    {
      fetch("validate-vehical-engine-number",{
      body:JSON.stringify({vehical_engine_number:Value}),
      method:'POST',
    }
    )
      .then(res=>res.json()).then(data=>
    {
      // console.log("fetching data from server by api"),
      // console.log("data",data);
      if(data.vehical_engine_number_error)
      { v_eng_no_Field_messg.innerHTML=`${data.vehical_engine_number_error}`;
        submitBtn.disabled = true;
      }
      else{
        v_eng_no_Field_messg.innerHTML=``;
      submitBtn.disabled = false;
      }
    })
    }
});

v_chass_no_Field.addEventListener("keyup",(e)=>{
    let Value=e.target.value;
    console.log(Value);
    console.log(Value.length);
    if(Value.length>0)
    {
      fetch("validate-vehical-chassics-number",{
      body:JSON.stringify({vehical_chassics_number:Value}),
      method:'POST',
    }
    )
      .then(res=>res.json()).then(data=>
    {
      // console.log("fetching data from server by api"),
      // console.log("data",data);
      if(data.vehical_chassics_number_error)
      { v_chass_no_Field_messg.innerHTML=`${data.vehical_chassics_number_error}`;
        submitBtn.disabled = true;
      }
      else{
        v_chass_no_Field_messg.innerHTML=``;
      submitBtn.disabled = false;
      }
    })
    }
});

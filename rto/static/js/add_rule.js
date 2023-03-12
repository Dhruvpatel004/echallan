let rcode_Field = document.querySelector("#rcode");

let rcode_Field_messg = document.querySelector("#rcode_check");

let submitBtn = document.querySelector("#submitBtn");

rcode_Field.addEventListener("keyup",(e)=>{
    let Value=e.target.value;
    console.log(Value);
    console.log(Value.length);
    if(Value.length>0)
    {
      fetch("validate-rule-code",{
      body:JSON.stringify({rule_code:Value}),
      method:'POST',
    }
    )
      .then(res=>res.json()).then(data=>
    {
      console.log("fetching data from server by api"),
      console.log("data",data);
      if(data.rule_code_error)
      { rcode_Field_messg.innerHTML=`${data.rule_code_error}`;
        submitBtn.disabled = true;
      }
      else{
        rcode_Field_messg.innerHTML=``;
      submitBtn.disabled = false;
      }
    })
    }
});
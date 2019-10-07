const $ = require('jquery')
const request = require('request');
const { exec } = require('child_process');


$('#ret').on('click',()=>{
  var age= $('#Starting_Balance').val()
  var name=$('#name').val()
  var aadhar_no = $('#aadhar_no').val()
  var phone = $('#phone').val()
  var nominee =$('#Nominee').val()
  console.log('hello')
  $("#enterdata").hide()
  $('#loader').show()

exec('python3 finger.py hola', (err, stdout, stderr) => {
  if (err) {
    return;
  }
  else {
    exec('python3 connector.py ' + aadhar_no + ' ' +age+' ' + name +' ' +phone, (err, stdout, stderr) => {
      if (err) {
        return;
      }
      console.log(stdout)
      $('#yo').text(stdout)
      $('#loader').hide()
      $('#data').show()
      $('#yo').show()


    })
  }
});
console.log(aadhar_no+' '+ age)

})


$('#reto').on('click',()=>{
  $('#data').hide()
  $('#enterdata').show()
}
)

$('#OP').on('click',()=>{
  window.open("to.html");
})
$('#OPP').on('click',()=>{
  console.log('harsh')
  var amount= $('#amount').val()
  var account=$('#account').val()
  exec('python3 connector2.py '+account+' '+amount, (err, stdout, stderr) => {
    if (err) {
      return;
    }
    else{
    alert(stdout)
}

  })

})

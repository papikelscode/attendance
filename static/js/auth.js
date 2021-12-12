const ClockIn = async () =>{
      let resContainer =    document.getElementById('response')
      let removeuserid = document.getElementById('enter-id')
      let inputcontainer = document.getElementById('staffID')
      const Data = {}
      Data.idnumber = staffID.value
      const res = await axios.post('/clockin',Data,{
                headers:{
                    'Content-Type':'application/json'
                }
      })
            if (res.data.status == 200){
            inputcontainer.classList.remove('error-is-red')
            removeuserid.style.visibility = "hidden"
            resContainer.style.color = "green"
            resContainer.style.visibility = "visible"
            resContainer.innerText = "Clock In Successful!" 
            }
            if (res.data.status == 404){
            inputcontainer.classList.add('error-is-red')
            removeuserid.style.visibility = "hidden"
            resContainer.style.color = "red"
            resContainer.style.visibility = "visible"
            resContainer.innerText = "Invalid ID Number!"  
            }
      
            if (staffID.value == ""){
            removeuserid.style.visibility = "hidden"
            resContainer.style.color = "red"
            resContainer.style.visibility = "visible"
            resContainer.innerText = "Please enter a user ID"  
}
}
const ClockOut = async () => {
    let resContainer =    document.getElementById('response')
    let removeuserid = document.getElementById('enter-id')
    let inputcontainer = document.getElementById('staffID')
    const Data = {}
    Data.idnumber = staffID.value
    const res = await axios.put('/clockout', Data, {
          headers: {
                'content-Type': 'application/json'
          }
    })
    if (res.data.status == 200){
        inputcontainer.classList.remove('error-is-red')
        removeuserid.style.visibility = "hidden"
        resContainer.style.color = "green"
        resContainer.style.visibility = "visible"
        resContainer.innerText = "Clock Out Successful!" 
        }
        if (res.data.status == 404){
        inputcontainer.classList.add('error-is-red')
        removeuserid.style.visibility = "hidden"
        resContainer.style.color = "red"
        resContainer.style.visibility = "visible"
        resContainer.innerText = "User didn't clock in!"  
        }
     
        if (staffID.value == ""){
        removeuserid.style.visibility = "hidden"
        resContainer.style.color = "red"
        resContainer.style.visibility = "visible"
        resContainer.innerText = "Please enter a user ID"  
}
}

const ModalHandler = (id) =>{
      const modal = document.getElementById(id)
      if(modal.classList.contains("is-active")){
      modal.classList.remove('is-active')
      }
      else(
          modal.classList.add('is-active')
      )
  }


const Login = async () =>{
    let loginstatus = document.getElementById('login-status')
    const Data = {}
    Data.idnumber = idnumber.value
    Data.password = password.value
    const res = await axios.post('/login',Data,{
        headers:{
            'Content-Type':'application/json'
        }
    
    })

    if(res.data.status == 200){
        loginstatus.style.color = "green"
        loginstatus.innerText = "WELCOME"
        window.location = '/dashboard'
    }

    if(res.data.status == 404){
        loginstatus.style.color = "red"
        loginstatus.innerText = "Incorrect username/password"
    }

    if(password.value == "" && idnumber.value == ""){
        loginstatus.style.color = "red"
        loginstatus.innerText = "Please fill out all fields"
    }

    

    console.log(res)
}

const InviteVisitor = async () => {
    try {
          const btn = document.getElementById('invitebtn')
          btn.classList.add('is-loading')
          const data = {}
          data.fname = document.getElementById('fname').value
          data.lname = document.getElementById('lname').value
          data.phone = document.getElementById('phone').value
          data.email = document.getElementById('email').value
          const response = await axios.post('/invite', data, {
                headers: {
                      'content-Type': 'application/json'
                }

          })
          if(response.data.status == 200){
                document.getElementById('login-notice-container').innerText = "Invite sent"
                btn.classList.remove('is-loading')
          }

          if(response.data.status == 500){
                document.getElementById('login-notice-container').innerText = "Sorry something went wrong!!!"
                btn.classList.remove('is-loading')
          }
         
          console.log(response)
          
    } catch (error) {
          document.getElementById('login-notice-container').innerText = "Sorry something went wrong!!!"
      //     btn.classList.remove('is-loading')
          console.log(error);
    }
    
}




const AddVistorItem = async () => {
    try {
          const btn = document.getElementById('additembtn')
          btn.classList.add('is-loading')
          const data = {}
          data.itemname = document.getElementById('itemname').value
          data.invitecode = document.getElementById('invitecode').value

          const response = await axios.post('/additem', data, {
                headers: {
                      'content-Type': 'application/json'
                }

          })
          if(response.data.status == 200){
                document.getElementById('notifyitem').innerText = "Item added to guest luggage"
                btn.classList.remove('is-loading')
                btn.classList.add('bx-check')
                btn.classList.add('bx-tada')
          }

          if(response.data.status == 404){
                document.getElementById('notifyitem').innerText = "Sorry something went wrong!!!"
                btn.classList.remove('is-loading')
          }
         
          console.log(response)
          
    } catch (error) {
          document.getElementById('notifyitem').innerText = "Sorry something went wrong!!!"
          btn.classList.remove('is-loading')
          console.log(error);
    }
    
}




const AddItemModal = (id,inviteid) => {
    document.getElementById('invitecode').value = inviteid
    const modal = document.getElementById(id)
    if (modal.classList.contains('is-active')) {
          modal.classList.remove('is-active')
    }
    else {
          modal.classList.add('is-active')
    }

}


const ShowItem  = async (id) =>{
    const response = await axios.get('/visitorsitem/'+id)
    document.getElementById('itemsTable').innerHTML = response.data
    document.getElementById('viewitems').classList.add('is-active')
}

const ChangePasword = async() =>{
    const data = {}
    data.currentpassword = document.getElementById('currentpassword').value
    data.password = document.getElementById('password').value
    data.conpassword = document.getElementById('conpassword').value
    const response = await axios.post('/password',data,{
          headers: {
                'content-Type': 'application/json'
          }
    })

    console.log(response);

}


const ClockVisitor = async (invitecode) =>{
      const response = await axios.get('/clockvisitor/'+invitecode)
      if(response.data.status == 200){
            alert("Operation completed")
      }
}
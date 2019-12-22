// swami hari
const express=require("express");
const app= express();
const bodyParser=require('body-parser');
const mongoose=require("mongoose");

const User=require("./model/data");
//const Sub=require("./models/Subs");
const path=require("path");
//const nodemailer=require("nodemailer");
const config=require("./config/key");
const cors=require("cors")

// Database
const db=async()=>{
    await mongoose.connect(config.connectionKey,{useNewUrlParser:true})
    console.log("Connection Success!")
 }
 db().catch(err=>console.log("err"))


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));

app.use(cors())


app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', '*'); //// Website you wish to allow to connect   
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');  // methods to allowed  
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');// Request headers you wish to allow     
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});
// @@@@@@@@@@@@ API ENDPOINTS @@@@@@@@@@@@


app.get("/hi",(req,res)=>{
 
   res.sendFile(path.join(__dirname,"/public/MIT/Landing page/home.html"))
})

app.post("/web",async(req,res)=>{
    User.remove({},(err,datas)=>{
        if(err)console.log(err)
        else{
            console.log("delete:",datas)

        const data={data:req.body}
    console.log(data)
    const user=new User(data)
    user.save().then(res=>console.log("saved to database")).catch(err=>console.log(err))
    
    res.json({msg:"all good"})
        }
    })
    

   
})

app.get("/web",async(req,res)=>{
   
  User.find({},(err,data)=>{
      if(err)console.log(err)
      else{
        res.setHeader("content-type", "application/json")

        //  console.log(data);
        res.send(JSON.stringify(data));
      }
  })
  
})

app.post("/home",(req,res)=>{
    console.log(req.body)
    const data=req.body
    console.log(req.body)
    res.json({msg:"succes",data})
})


// @@@@@@@@ server Runnig @@@@@@@@@@@@
const port=process.env.NODE_ENV || 8000
app.listen(port,()=>{
    console.log("Server Running Successfully on port:",port);
})


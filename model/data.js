const mongoose=require("mongoose")
const Schema=mongoose.Schema

const nameSchme=new Schema({
    data:{
        type:Array
    }
})

module.exports=mongoose.model("coll",nameSchme)
import axios from 'axios';  //引入axios
import qs from "qs";      //引入qs依赖
// import app from '../main'    可以根据项目需求进行引入

const service = axios.create({
  headers:{
    "Access-Control-Allow-Origin":"*",
    "accept": "*/*",
          },
    //baseURL :不进行配置
    // baseURL: '/test',  // api的base_url
    timeout: 3000000,  // 请求超时时间
    withCredentials : true
});
//上传文件时不能使用qs去修改默认的上传数据，contype-content 不设置


export default service;

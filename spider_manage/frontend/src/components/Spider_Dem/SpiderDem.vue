<template>
    <div id="sdxy">
        <h2>{{this.$route.query.compantName}}爬虫程序数据演示</h2>
        <br>
        <div>
          <div class="icon-close">
            <a href="javascript:void(0)"><i class="el-icon-close"></i></a></div>

        <div class="Tips">
            <i class="el-icon-chat-dot-square"></i>
            <span >温馨提示!</span>
          <br>
          <br>
          <span>本页面可以通过在下方输入企业名称点击启动按钮实现实时爬虫程序进行实时抓取数据信息演示，仅作展示参考，
          不具有存储数据功能。</span>
        </div>

        </div>

      <br>
      <br>
          <el-input v-model="input" placeholder="请输入需要查询的公司名称" style="width: 260px;left: -500px"></el-input>

        <div class="header" >
          <a href="javascript:void(0);" @click="test()"><i>点击查询</i><i class="el-icon-caret-right"></i></a>
        </div>

        <!--左侧结果栏-->
        <div></div>
        <!--右侧样例-->
      <br>
      <br>
      <hr style="width: 99%; font-size: 15px; color:red; font-weight: bold"/>
      <div style="margin-left: 30px">
        <h3 style="font-size: 25px;text-align: left;transform: translateY(30px)">查询结果：</h3>
        <h3 style="font-size: 25px;margin-left: 10%;">样例结果展示：</h3>
      </div>
      <!--<div>-->
        <div class="casedatas">
            <pre v-for="(item,index) in casedata">
            {{index}} : {{item}}
          </pre>
        </div>
       <div class="result" v-if="resultTAG">
          <pre v-for="(item,index) in results">
           {{index}} : {{item}}
          </pre>
      </div>
      <!--</div>-->
      <div class="loading" v-if="loads">
        <div></div>
        正在查询，请稍后。。。
      </div>

    </div>
</template>

<script>

  import {post}from '../../axios/api'
    export default {
        name: "SpiderDem",
      data(){
          return{
              input: '',
              casedata :{
                "公司名":"阿里巴巴（中国）网络技术有限公司",
                "注册资本":"512233.000000万美元",
                "实缴资本":"59690.0万美元",
                "统一社会信用代码":"91330100716105852F"
                },
              resultTAG :true,
              results:null,
              loads:false,
              urls: this.$route.query.url
          }
      },
      methods:{
          async test(){
            // const url = '/test/crawler/sdxy_data_search';
            const url = this.urls;
            let formData = new FormData();

            this.userid = this.input;
            formData.append("company",this.userid);
             debugger;
             this.loads = true;
            let resp = await post(url,formData);
            this.loads = false;
            debugger;

            console.log(resp.data);
            if (resp.data.data){
              this.results = resp.data.data
            }else{
              this.results = resp.data.err_msg
            }
          },
        }


    }
</script>

<style scoped lang="scss">
  #sdxy{
    margin: 0;
    padding: 0;
    width: 100%;
    line-height: 100%;
    background-color: #ECF0F5;

  .header{
    float: left;
    justify-content: center;
    /*background-color: purple;*/

    top: 0;
    /*width: 45px;*/
    /*height: 30px;*/
    transform: translate(560px,5px);
    -webkit-transform: translate(560px,5px);
    -ms-transform: translate(560px,5px);
    i{
      font-size:30px;
      font-weight: bold;
      color: #5A8C5A;
      font-style:normal;
    }
  }
  }
  .Tips{
    text-align: left;
    height: 120px;
    background-color: #40BAF5;
    width: 99%;

    i{
      font-size:30px;
      font-weight: bold;
      color: #E0EDFB;
      margin-left: 20px;
      margin-top: 15px;
    }
    span:nth-child(2){
      margin-left: 15px;
      font-size: 25px;
      color: #FFFFFF;
      font-weight:bold;
    }
    span:nth-child(5){
      margin-left: 90px;
      font-size: 16px;
      color: #FFFFFF;
      font-weight:bold;
    }
  }
  .icon-close{
      margin-right: 30px;
      margin-top: 10px;
      float: right;
      z-index: 300;
     i{
       font-size: 15px;
        color:#FFFFFF; ;
     }
    }
  .casedatas{
    /*float: left;*/
    margin-left: 46%;
    color: #BC402C;
    font-size: 16px;
    position: absolute;
    width: 42%;
  }
  .result{
    float: left;
    margin-left: 10px;
    overflow:auto;
    height: 400px;
    color: #6364A7;
    font-size: 16px;
    line-height: 30px;
    width: 50%;
    padding: 10px;
  }
   pre{
      width:100%;
      text-align: justify;
      word-break: break-all;
      word-wrap: break-word;
      white-space: pre-wrap;
  };
  .loading{
    width: 400px;
    height: 300px;
    margin: 0 auto;
    opacity: 0.99;
    /*background-color: lawngreen;*/
    padding-top: 1px; //防止上边框和盒子中的选择图形上边框重叠引起的问题
    transform: translateX(-100px);
    div{
      border-radius: 50%;
      width:50px;
      height: 50px;
      border-top:10px solid red;
      border-left:10px solid slategrey;
      border-right: 10px solid chocolate;
      border-bottom: 10px solid navy;
      margin-left: 150px;
      margin-top: 90px;

       animation:turn 1s linear infinite;
            @keyframes turn{
      0%{-webkit-transform:rotate(0deg);}
      25%{-webkit-transform:rotate(90deg);}
      50%{-webkit-transform:rotate(180deg);}
      75%{-webkit-transform:rotate(270deg);}
      100%{-webkit-transform:rotate(360deg);}
    }
    };
  }
</style>

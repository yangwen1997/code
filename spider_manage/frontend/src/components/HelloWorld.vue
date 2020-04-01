<template>
  <el-container>
    <!--左侧导航菜单-->
    <el-aside style="width: 230px;height: 900px">

      <el-radio-group v-model="isCollapse" style="margin-bottom: 20px;">
        <el-radio-button :label="false">展开</el-radio-button>
        <el-radio-button :label="true">收起</el-radio-button>
      </el-radio-group>

      <el-menu :default-active="activeIndex" class="el-menu-vertical-demo" :collapse="isCollapse" text-color="#4047F5" @select="handleSelect">

        <el-submenu index="1">
          <template slot="title">
            <i class="el-icon-location"></i>
            <span slot="title">爬虫数据程序演示</span>
          </template>

          <el-menu-item-group>
            <el-submenu index="1-2">
            <span slot="title">企查查程序</span>
            <el-menu-item index="1-2-1">企查查基本信息演示</el-menu-item>
          </el-submenu >
            <el-submenu index="1-3">
            <span slot="title">水滴信用程序</span>
            <el-menu-item index="1-3-1" >水滴信用基本信息演示</el-menu-item>
          </el-submenu>
            <el-submenu index="1-4">
            <span slot="title">百度信用程序</span>
            <el-menu-item index="1-4-1">百度信用基本信息演示</el-menu-item>
          </el-submenu>
            <el-submenu index="1-5">
            <span slot="title">天眼查</span>
            <el-menu-item index="1-5-1">天眼查基本信息演示</el-menu-item>
          </el-submenu>
          </el-menu-item-group>


        </el-submenu>

        <el-menu-item index="2">
          <i class="el-icon-menu"></i>
          <span slot="title">导航二</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
          <i class="el-icon-document"></i>
          <span slot="title">导航三</span>
        </el-menu-item>
        <el-menu-item index="4">
          <i class="el-icon-setting"></i>
          <span slot="title">导航四</span>
        </el-menu-item>
      </el-menu>

    </el-aside>

    <!---->
    <el-container>
      <!--顶部不变-->
      <el-header>
        <a href="#" class="logo"> 爬虫监控平台程序</a>
       </el-header>

      <!--组件视图-->
      <el-main ><router-view/></el-main>

      <!--底部，不展示-->
      <!--<el-footer>Footer</el-footer>-->
    </el-container>

</el-container>
</template>

<script>
  export default {
    name:"HelloWorld",
     data() {
      return {
        isCollapse: true,
        activeIndex:"1",
        compantName:""
      };
    },
     methods: {
       handleSelect(val,path){
        if (val == '1-2-1'){
          this.compantName = "企查查";
          this.$router.push({path:'/Spider',query:{"compantName":this.compantName}})
        }else if(val == '1-3-1'){
          this.compantName = "水滴信用";
          this.$router.push({path:'/Spider',query:{"compantName":this.compantName,"url":"/test/crawler/sdxy_data_search"}})
        }else if(val == '1-4-1'){
          this.compantName = "百度信用";
          this.$router.push({path:'/Spider',query:{"compantName":this.compantName}})
        }else if(val == '1-5-1'){
          this.compantName = "天眼查";
          this.$router.push({path:'/Spider',query:{"compantName":this.compantName}})
        }

        console.log(val)

        // debugger;
      },
    }
  }
</script>

<style lang="scss" scoped>

  /*.el-container{*/
     /*min-height: 100%;*/
    /*height: 100%;*/
    /*position: relative;*/
  /*}*/
  .el-aside{
    /*position: fixed;*/
    position: absolute;
    top: 59px;
    left: 0;
    padding: 50px 0 0 0;
    /*padding-top: 50px;*/
    min-height: 100%;
    height:auto;
    background-color: #222d32;
    width: 230px;
    z-index: 810;
  }
  .el-header{
    background-color: #40BAF5;
    text-align: left;
    margin: 0;
    padding: 0;
    .logo{
      width: 230px;

      overflow: hidden;
      font-size: 20px;
     line-height: 50px;
      color: #fff
    }
      a{
        cursor: pointer;
      }
    left: 0;

  }
  .el-main{
    right: 0;
    /*width: 80%;*/
    margin: 0 0 0 230px;
    padding: 0;
    /*margin-left: 230px;*/
    /*line-height:778px;*/
    /*position: fixed;*/
    overflow-x: hidden;

  }

  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;

  }

</style>

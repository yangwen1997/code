webpackJsonp([1],{"6aoz":function(t,e){},NHnr:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("7+uW"),s={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("router-view")],1)},staticRenderFns:[]};var l=a("VU/8")({name:"App"},s,!1,function(t){a("h3tY")},null,null).exports,i=a("/ocq"),r={name:"HelloWorld",data:function(){return{isCollapse:!0,activeIndex:"1",compantName:""}},methods:{handleSelect:function(t,e){"1-2-1"==t?(this.compantName="企查查",this.$router.push({path:"/Spider",query:{compantName:this.compantName}})):"1-3-1"==t?(this.compantName="水滴信用",this.$router.push({path:"/Spider",query:{compantName:this.compantName,url:["/crawler/sdxy_data_search","/crawler/sdxy_basic","3"]}})):"1-4-1"==t?(this.compantName="百度信用",this.$router.push({path:"/Spider",query:{compantName:this.compantName}})):"1-5-1"==t&&(this.compantName="天眼查",this.$router.push({path:"/Spider",query:{compantName:this.compantName}})),console.log(t)}}},o={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-container",[a("el-header",[a("a",{staticClass:"logo",attrs:{href:"#"}},[t._v(" 爬虫监控平台程序")])]),t._v(" "),a("el-aside",{staticStyle:{width:"230px",height:"900px"}},[a("el-radio-group",{staticStyle:{"margin-bottom":"20px"},model:{value:t.isCollapse,callback:function(e){t.isCollapse=e},expression:"isCollapse"}},[a("el-radio-button",{attrs:{label:!1}},[t._v("展开")]),t._v(" "),a("el-radio-button",{attrs:{label:!0}},[t._v("收起")])],1),t._v(" "),a("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"default-active":t.activeIndex,collapse:t.isCollapse,"text-color":"#4047F5"},on:{select:t.handleSelect}},[a("el-submenu",{attrs:{index:"1"}},[a("template",{slot:"title"},[a("i",{staticClass:"el-icon-location"}),t._v(" "),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("爬虫数据程序演示")])]),t._v(" "),a("el-menu-item-group",[a("el-submenu",{attrs:{index:"1-2"}},[a("span",{attrs:{slot:"title"},slot:"title"},[t._v("企查查程序")]),t._v(" "),a("el-menu-item",{attrs:{index:"1-2-1"}},[t._v("企查查基本信息演示")])],1),t._v(" "),a("el-submenu",{attrs:{index:"1-3"}},[a("span",{attrs:{slot:"title"},slot:"title"},[t._v("水滴信用程序")]),t._v(" "),a("el-menu-item",{attrs:{index:"1-3-1"}},[t._v("水滴信用基本信息演示")])],1),t._v(" "),a("el-submenu",{attrs:{index:"1-4"}},[a("span",{attrs:{slot:"title"},slot:"title"},[t._v("百度信用程序")]),t._v(" "),a("el-menu-item",{attrs:{index:"1-4-1"}},[t._v("百度信用基本信息演示")])],1),t._v(" "),a("el-submenu",{attrs:{index:"1-5"}},[a("span",{attrs:{slot:"title"},slot:"title"},[t._v("天眼查")]),t._v(" "),a("el-menu-item",{attrs:{index:"1-5-1"}},[t._v("天眼查基本信息演示")])],1)],1)],2),t._v(" "),a("el-menu-item",{attrs:{index:"2"}},[a("i",{staticClass:"el-icon-menu"}),t._v(" "),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("导航二")])]),t._v(" "),a("el-menu-item",{attrs:{index:"3",disabled:""}},[a("i",{staticClass:"el-icon-document"}),t._v(" "),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("导航三")])]),t._v(" "),a("el-menu-item",{attrs:{index:"4"}},[a("i",{staticClass:"el-icon-setting"}),t._v(" "),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("导航四")])])],1)],1),t._v(" "),a("el-main",[a("router-view")],1)],1)},staticRenderFns:[]};var u=a("VU/8")(r,o,!1,function(t){a("jzhX")},"data-v-85d4ec20",null).exports,c={render:function(){var t=this.$createElement;return(this._self._c||t)("div",[this._v('\n  {\n    "spider" :"sucess"\n    }\n')])},staticRenderFns:[]};a("VU/8")({name:"QccSpiderDem"},c,!1,function(t){a("oZKv")},"data-v-65f46fee",null).exports;var p=a("Xxa5"),d=a.n(p),v=a("exGp"),m=a.n(v),_=a("I29D"),h=a.n(_),f=(a("Xu0s"),h.a.create({headers:{"Access-Control-Allow-Origin":"*",accept:"*/*"},timeout:3e6,withCredentials:!0})),x=function(t,e){return f({url:t,method:"post",data:e})},b={name:"SpiderDem",data:function(){return{input_comename:"",casedata:{"公司名":"阿里巴巴（中国）网络技术有限公司","注册资本":"512233.000000万美元","实缴资本":"59690.0万美元","统一社会信用代码":"91330100716105852F"},resultTAG:!0,results:null,loads:!1,urls:"",options:[{value:"选项0",label:"全部信息查询"},{value:"选项1",label:"基本信息查询"}],value:""}},methods:{test:function(){var t=this;return m()(d.a.mark(function e(){var a,n,s;return d.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return(a=new FormData).append("company_name",t.input_comename),"选项0"==t.value||""==t.value?(n=t.$route.query.url[0],a.append("ApiType",t.options[0].label)):"选项1"==t.value&&(n=t.$route.query.url[1],a.append("ApiType",t.options[1].label)),t.loads=!0,e.next=7,x(n,a);case 7:s=e.sent,t.loads=!1,s.data.data?t.results=s.data.data:t.results=s.data.err_msg;case 10:case"end":return e.stop()}},e,t)}))()}}},y={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"sdxy"}},[a("div",{staticClass:"headerTop"},[a("h2",[t._v(t._s(this.$route.query.compantName)+"爬虫程序数据演示")]),t._v(" "),a("el-select",{attrs:{placeholder:"请选择查询的数据类型"},model:{value:t.value,callback:function(e){t.value=e},expression:"value"}},t._l(t.options,function(t){return a("el-option",{key:t.value,attrs:{label:t.label,value:t.value}})}),1),t._v(" "),a("el-input",{staticStyle:{width:"550px",left:"-90px",top:"98px"},attrs:{placeholder:"请输入需要查询的公司名称"},model:{value:t.input_comename,callback:function(e){t.input_comename=e},expression:"input_comename"}}),t._v(" "),a("el-button",{staticClass:"el-sercer",attrs:{type:"success"},on:{click:function(e){return t.test()}}},[a("a",{attrs:{href:"javascript:void(0)"}},[t._v("搜索")])])],1),t._v(" "),a("div"),t._v(" "),a("br"),t._v(" "),a("br"),t._v(" "),a("hr",{staticStyle:{width:"99%","font-size":"15px",color:"red","font-weight":"bold"}}),t._v(" "),t._m(0),t._v(" "),a("div",{staticClass:"casedatas"},t._l(t.casedata,function(e,n){return a("pre",[t._v("        "+t._s(n)+" : "+t._s(e)+"\n      ")])}),0),t._v(" "),t.resultTAG?a("div",{staticClass:"result"},t._l(t.results,function(e,n){return a("pre",[t._v("       "+t._s(n)+" : "+t._s(e)+"\n      ")])}),0):t._e(),t._v(" "),t.loads?a("div",{staticClass:"loading"},[a("p",[t._v("正在查询，请稍后。。。")]),t._v(" "),a("div")]):t._e()])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("div",{staticStyle:{"margin-left":"30px"}},[e("h3",{staticStyle:{"font-size":"25px","text-align":"left",transform:"translate(90px,30px)"}},[this._v("查询结果：")]),this._v(" "),e("h3",{staticStyle:{"font-size":"25px","margin-left":"30%"}},[this._v("样例结果展示：")])])}]};var C=a("VU/8")(b,y,!1,function(t){a("iXjK")},"data-v-d3e23296",null).exports;n.default.use(i.a);var S=new i.a({routes:[{path:"/",name:"HelloWorld",component:u,children:[{path:"/Spider",name:"SpiderDem",component:C}]}]}),w=a("zL8q"),N=a.n(w);a("tvR6"),a("6aoz");n.default.config.productionTip=!1,n.default.use(N.a),new n.default({el:"#app",router:S,render:function(t){return t(l)}})},h3tY:function(t,e){},iXjK:function(t,e){},jzhX:function(t,e){},oZKv:function(t,e){},tvR6:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.8ffd7047937acefb38dc.js.map
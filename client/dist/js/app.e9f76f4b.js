(function(e){function t(t){for(var i,o,a=t[0],l=t[1],u=t[2],p=0,c=[];p<a.length;p++)o=a[p],Object.prototype.hasOwnProperty.call(r,o)&&r[o]&&c.push(r[o][0]),r[o]=0;for(i in l)Object.prototype.hasOwnProperty.call(l,i)&&(e[i]=l[i]);h&&h(t);while(c.length)c.shift()();return s.push.apply(s,u||[]),n()}function n(){for(var e,t=0;t<s.length;t++){for(var n=s[t],i=!0,a=1;a<n.length;a++){var l=n[a];0!==r[l]&&(i=!1)}i&&(s.splice(t--,1),e=o(o.s=n[0]))}return e}var i={},r={app:0},s=[];function o(t){if(i[t])return i[t].exports;var n=i[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,o),n.l=!0,n.exports}o.m=e,o.c=i,o.d=function(e,t,n){o.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.t=function(e,t){if(1&t&&(e=o(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(o.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)o.d(n,i,function(t){return e[t]}.bind(null,i));return n},o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,"a",t),t},o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},o.p="/";var a=window["webpackJsonp"]=window["webpackJsonp"]||[],l=a.push.bind(a);a.push=t,a=a.slice();for(var u=0;u<a.length;u++)t(a[u]);var h=l;s.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("56d7")},"034f":function(e,t,n){"use strict";n("85ec")},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var i=n("2b0e"),r=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("b-container",[n("Shell")],1)},s=[],o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("b-shell",{style:e.style,attrs:{banner:e.banner,shell_input:e.send_to_terminal,autofocus:""},on:{shell_output:e.prompt}})],1)},a=[],l=n("bc3a"),u=n.n(l),h=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{on:{click:function(t){return e.$refs.cmd.focus()}}},[n("div",{ref:"terminal",attrs:{id:"container"}},[e.banner?n("div",{attrs:{id:"banner"}},[n("p",[e.banner.img?n("img",{attrs:{align:e.banner.img.align?e.banner.img.align:"left",src:e.banner.img.link?e.banner.img.link:"@/logo.png",width:e.banner.img.width?e.banner.img.width:"100px",height:e.banner.img.height?e.banner.img.height:"100px"}}):e._e()]),e.banner.header?n("h2",{staticStyle:{"letter-spacing":"4px"}},[e._v(e._s(e.banner.header))]):e._e(),e.banner.subHeader?n("p",[e._v(e._s(e.banner.subHeader))]):e._e(),e.banner.helpHeader?n("p",[e._v(e._s(e.banner.helpHeader))]):e._e(),n("p")]):e._e(),n("output",{ref:"output"}),n("div",{staticClass:"input-line",attrs:{id:"input-line"}},[n("div",{staticClass:"prompt"},[e.banner.emoji.first&&e.showemoji?n("div",[e._v("("+e._s(e.banner.emoji.first)+")")]):e._e(),e.banner.emoji.second&&!e.showemoji?n("div",[e._v("("+e._s(e.banner.emoji.second)+")")]):e._e(),n("div",[e._v(e._s(e.banner.sign?e.banner.sign:">"))])]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.value,expression:"value"}],ref:"cmd",staticClass:"cmdline",attrs:{autofocus:""},domProps:{value:e.value},on:{keydown:[function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.cmd_enter(t)},function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"up",38,t.key,["Up","ArrowUp"])?null:e.history_up()},function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"down",40,t.key,["Down","ArrowDown"])?null:e.history_down()},function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"tab",9,t.key,"Tab")?null:e.cmd_tab(t)}],input:function(t){t.target.composing||(e.value=t.target.value)}}}),n("next_line")],1)])])},p=[],c=(n("498a"),{props:{shell_input:{required:!1},banner:{type:Object,required:!1,default:function(){return{header:"Vue Shell",subHeader:"Shell is power just enjoy 🔥",helpHeader:'Enter "help" for more information.',emoji:{first:"🔅",second:"🔆",time:750},sign:"VueShell $",img:{align:"left",link:"@/logo.png",width:100,height:100}}}},commands:{type:Array}},data:function(){return{showemoji:!0,value:"",history_:[],histpos_:0,histtemp_:0}},watch:{shell_input:function(e){this.output(e),this.$parent.send_to_terminal=""}},methods:{history_up:function(){this.history_.length&&(this.history_[this.histpos_]?this.history_[this.histpos_]=this.value:this.histtemp_=this.value),this.histpos_--,this.histpos_<0&&(this.histpos_=0),this.value=this.history_[this.histpos_]?this.history_[this.histpos_]:this.histtemp_},history_down:function(){this.history_.length&&(this.history_[this.histpos_]?this.history_[this.histpos_]=this.value:this.histtemp_=this.value),this.histpos_++,this.histpos_>this.history_.length&&(this.histpos_=this.history_.length),this.value=this.history_[this.histpos_]?this.history_[this.histpos_]:this.histtemp_},cmd_tab:function(e){e.preventDefault()},cmd_enter:function(){this.value&&(this.history_[this.history_.length]=this.value,this.histpos_=this.history_.length);var e=this.$refs.cmd.parentNode.cloneNode(!0);e.removeAttribute("id"),e.classList.add("line");var t=e.querySelector("input.cmdline");t.autofocus=!1,t.readOnly=!0,this.$refs.output.appendChild(e),""!=this.value.trim()&&this.$emit("shell_output",this.value),this.value=""},output:function(e){this.$refs.output.insertAdjacentHTML("beforeEnd","<pre>"+e+"</pre>"),this.value="";var t=this.$el.getElementsByClassName("prompt"),n=t[t.length-1];console.log(n),n.scrollIntoView({behavior:"smooth"})}},mounted:function(){var e=this;this.banner.emoji.first&&this.banner.emoji.second&&this.banner.emoji.time&&setInterval((function(){e.showemoji=!e.showemoji}),this.banner.emoji.time)}}),d=c,_=(n("8c0f"),n("2877")),f=Object(_["a"])(d,h,p,!1,null,"64a39c56",null),m=f.exports,b=n("75ba");i["a"].component("b-shell",m),i["a"].use(m);var y={name:"Vue",data:function(){return{style:{width:"800px"},send_to_terminal:"",wating_prompt:"typing...",user_prompt:"> ",banner:{header:"AlbertoBot v0.0.1",subHeader:"This bot tells you information about me.",helpHeader:"> Hello! What is your name?",emoji:{first:""},sign:"> "},prologue:"",bot_lines:["Hello! What is your name?"],user_lines:[]}},methods:{prompt:function(e){var t=this;1==this.$children[0].history_.length&&(e=b.capitalizeFirstLetter(e),this.prologue="When the user is asked their name, they reply: '".concat(e,"'.")),this.user_lines.push(e);var n={bot_lines:this.bot_lines,user_lines:this.user_lines,prologue:this.prologue,query:e};this.banner.sign=this.wating_prompt,u.a.post("api/query",n).then((function(e){console.log(e);var n=e["data"]["reply"];t.send_to_terminal="> "+n,t.bot_lines.push(n),t.banner.sign=t.user_prompt})).catch((function(e){console.log(e),t.banner.sign=t.user_prompt,t.send_to_terminal="This website is under maintenance. Please check again later"}))}}},v=y,g=Object(_["a"])(v,o,a,!1,null,null,null),w=g.exports,j={name:"App",components:{Shell:w},created:function(){document.title="AlbertoBot"}},k=j,x=(n("034f"),Object(_["a"])(k,r,s,!1,null,null,null)),O=x.exports;i["a"].config.productionTip=!1,new i["a"]({render:function(e){return e(O)}}).$mount("#app")},"661a":function(e,t,n){},"75ba":function(e,t,n){function i(e){return e.charAt(0).toUpperCase()+e.slice(1)}n("fb6a"),e.exports={capitalizeFirstLetter:function(e){return i(e)}}},"85ec":function(e,t,n){},"8c0f":function(e,t,n){"use strict";n("661a")}});
//# sourceMappingURL=app.e9f76f4b.js.map
(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[888],{1859:function(e,t,r){"use strict";r.d(t,{Z:function(){return re}});var n=r(1526),a=Math.abs,o=String.fromCharCode;function c(e){return e.trim()}function s(e,t,r){return e.replace(t,r)}function i(e,t){return e.indexOf(t)}function u(e,t){return 0|e.charCodeAt(t)}function f(e,t,r){return e.slice(t,r)}function l(e){return e.length}function p(e){return e.length}function d(e,t){return t.push(e),e}var y=1,h=1,m=0,v=0,g=0,b="";function w(e,t,r,n,a,o,c){return{value:e,root:t,parent:r,type:n,props:a,children:o,line:y,column:h,length:c,return:""}}function x(e,t,r){return w(e,t.root,t.parent,r,t.props,t.children,0)}function $(){return g=v>0?u(b,--v):0,h--,10===g&&(h=1,y--),g}function S(){return g=v<m?u(b,v++):0,h++,10===g&&(h=1,y++),g}function k(){return u(b,v)}function O(){return v}function C(e,t){return f(b,e,t)}function P(e){switch(e){case 0:case 9:case 10:case 13:case 32:return 5;case 33:case 43:case 44:case 47:case 62:case 64:case 126:case 59:case 123:case 125:return 4;case 58:return 3;case 34:case 39:case 40:case 91:return 2;case 41:case 93:return 1}return 0}function _(e){return y=h=1,m=l(b=e),v=0,[]}function E(e){return b="",e}function j(e){return c(C(v-1,N(91===e?e+2:40===e?e+1:e)))}function A(e){for(;(g=k())&&g<33;)S();return P(e)>2||P(g)>3?"":" "}function M(e,t){for(;--t&&S()&&!(g<48||g>102||g>57&&g<65||g>70&&g<97););return C(e,O()+(t<6&&32==k()&&32==S()))}function N(e){for(;S();)switch(g){case e:return v;case 34:case 39:return N(34===e||39===e?e:g);case 40:41===e&&N(e);break;case 92:S()}return v}function T(e,t){for(;S()&&e+g!==57&&(e+g!==84||47!==k()););return"/*"+C(t,v-1)+"*"+o(47===e?e:S())}function R(e){for(;!P(k());)S();return C(e,v)}var z="-ms-",D="-moz-",F="-webkit-",I="comm",L="rule",Z="decl";function G(e,t){for(var r="",n=p(e),a=0;a<n;a++)r+=t(e[a],a,e,t)||"";return r}function B(e,t,r,n){switch(e.type){case"@import":case Z:return e.return=e.return||e.value;case I:return"";case L:e.value=e.props.join(",")}return l(r=G(e.children,n))?e.return=e.value+"{"+r+"}":""}function W(e,t){switch(function(e,t){return(((t<<2^u(e,0))<<2^u(e,1))<<2^u(e,2))<<2^u(e,3)}(e,t)){case 5103:return F+"print-"+e+e;case 5737:case 4201:case 3177:case 3433:case 1641:case 4457:case 2921:case 5572:case 6356:case 5844:case 3191:case 6645:case 3005:case 6391:case 5879:case 5623:case 6135:case 4599:case 4855:case 4215:case 6389:case 5109:case 5365:case 5621:case 3829:return F+e+e;case 5349:case 4246:case 4810:case 6968:case 2756:return F+e+D+e+z+e+e;case 6828:case 4268:return F+e+z+e+e;case 6165:return F+e+z+"flex-"+e+e;case 5187:return F+e+s(e,/(\w+).+(:[^]+)/,"-webkit-box-$1$2-ms-flex-$1$2")+e;case 5443:return F+e+z+"flex-item-"+s(e,/flex-|-self/,"")+e;case 4675:return F+e+z+"flex-line-pack"+s(e,/align-content|flex-|-self/,"")+e;case 5548:return F+e+z+s(e,"shrink","negative")+e;case 5292:return F+e+z+s(e,"basis","preferred-size")+e;case 6060:return F+"box-"+s(e,"-grow","")+F+e+z+s(e,"grow","positive")+e;case 4554:return F+s(e,/([^-])(transform)/g,"$1-webkit-$2")+e;case 6187:return s(s(s(e,/(zoom-|grab)/,F+"$1"),/(image-set)/,F+"$1"),e,"")+e;case 5495:case 3959:return s(e,/(image-set\([^]*)/,F+"$1$`$1");case 4968:return s(s(e,/(.+:)(flex-)?(.*)/,"-webkit-box-pack:$3-ms-flex-pack:$3"),/s.+-b[^;]+/,"justify")+F+e+e;case 4095:case 3583:case 4068:case 2532:return s(e,/(.+)-inline(.+)/,F+"$1$2")+e;case 8116:case 7059:case 5753:case 5535:case 5445:case 5701:case 4933:case 4677:case 5533:case 5789:case 5021:case 4765:if(l(e)-1-t>6)switch(u(e,t+1)){case 109:if(45!==u(e,t+4))break;case 102:return s(e,/(.+:)(.+)-([^]+)/,"$1-webkit-$2-$3$1"+D+(108==u(e,t+3)?"$3":"$2-$3"))+e;case 115:return~i(e,"stretch")?W(s(e,"stretch","fill-available"),t)+e:e}break;case 4949:if(115!==u(e,t+1))break;case 6444:switch(u(e,l(e)-3-(~i(e,"!important")&&10))){case 107:return s(e,":",":"+F)+e;case 101:return s(e,/(.+:)([^;!]+)(;|!.+)?/,"$1"+F+(45===u(e,14)?"inline-":"")+"box$3$1"+F+"$2$3$1"+z+"$2box$3")+e}break;case 5936:switch(u(e,t+11)){case 114:return F+e+z+s(e,/[svh]\w+-[tblr]{2}/,"tb")+e;case 108:return F+e+z+s(e,/[svh]\w+-[tblr]{2}/,"tb-rl")+e;case 45:return F+e+z+s(e,/[svh]\w+-[tblr]{2}/,"lr")+e}return F+e+z+e+e}return e}function q(e){return E(X("",null,null,null,[""],e=_(e),0,[0],e))}function X(e,t,r,n,a,c,i,u,f){for(var p=0,y=0,h=i,m=0,v=0,g=0,b=1,w=1,x=1,C=0,P="",_=a,E=c,N=n,z=P;w;)switch(g=C,C=S()){case 34:case 39:case 91:case 40:z+=j(C);break;case 9:case 10:case 13:case 32:z+=A(g);break;case 92:z+=M(O()-1,7);continue;case 47:switch(k()){case 42:case 47:d(U(T(S(),O()),t,r),f);break;default:z+="/"}break;case 123*b:u[p++]=l(z)*x;case 125*b:case 59:case 0:switch(C){case 0:case 125:w=0;case 59+y:v>0&&l(z)-h&&d(v>32?K(z+";",n,r,h-1):K(s(z," ","")+";",n,r,h-2),f);break;case 59:z+=";";default:if(d(N=H(z,t,r,p,y,a,u,P,_=[],E=[],h),c),123===C)if(0===y)X(z,t,N,N,_,c,h,u,E);else switch(m){case 100:case 109:case 115:X(e,N,N,n&&d(H(e,N,N,0,0,a,u,P,a,_=[],h),E),a,E,h,u,n?_:E);break;default:X(z,N,N,N,[""],E,h,u,E)}}p=y=v=0,b=x=1,P=z="",h=i;break;case 58:h=1+l(z),v=g;default:if(b<1)if(123==C)--b;else if(125==C&&0==b++&&125==$())continue;switch(z+=o(C),C*b){case 38:x=y>0?1:(z+="\f",-1);break;case 44:u[p++]=(l(z)-1)*x,x=1;break;case 64:45===k()&&(z+=j(S())),m=k(),y=l(P=z+=R(O())),C++;break;case 45:45===g&&2==l(z)&&(b=0)}}return c}function H(e,t,r,n,o,i,u,l,d,y,h){for(var m=o-1,v=0===o?i:[""],g=p(v),b=0,x=0,$=0;b<n;++b)for(var S=0,k=f(e,m+1,m=a(x=u[b])),O=e;S<g;++S)(O=c(x>0?v[S]+" "+k:s(k,/&\f/g,v[S])))&&(d[$++]=O);return w(e,t,r,0===o?L:l,d,y,h)}function U(e,t,r){return w(e,t,r,I,o(g),f(e,2,-2),0)}function K(e,t,r,n){return w(e,t,r,Z,f(e,0,n),f(e,n+1,-1),n)}var V=function(e,t,r){for(var n=0,a=0;n=a,a=k(),38===n&&12===a&&(t[r]=1),!P(a);)S();return C(e,v)},Y=function(e,t){return E(function(e,t){var r=-1,n=44;do{switch(P(n)){case 0:38===n&&12===k()&&(t[r]=1),e[r]+=V(v-1,t,r);break;case 2:e[r]+=j(n);break;case 4:if(44===n){e[++r]=58===k()?"&\f":"",t[r]=e[r].length;break}default:e[r]+=o(n)}}while(n=S());return e}(_(e),t))},J=new WeakMap,Q=function(e){if("rule"===e.type&&e.parent&&e.length){for(var t=e.value,r=e.parent,n=e.column===r.column&&e.line===r.line;"rule"!==r.type;)if(!(r=r.parent))return;if((1!==e.props.length||58===t.charCodeAt(0)||J.get(r))&&!n){J.set(e,!0);for(var a=[],o=Y(t,a),c=r.props,s=0,i=0;s<o.length;s++)for(var u=0;u<c.length;u++,i++)e.props[i]=a[s]?o[s].replace(/&\f/g,c[u]):c[u]+" "+o[s]}}},ee=function(e){if("decl"===e.type){var t=e.value;108===t.charCodeAt(0)&&98===t.charCodeAt(2)&&(e.return="",e.value="")}},te=[function(e,t,r,n){if(!e.return)switch(e.type){case Z:e.return=W(e.value,e.length);break;case"@keyframes":return G([x(s(e.value,"@","@"+F),e,"")],n);case L:if(e.length)return function(e,t){return e.map(t).join("")}(e.props,(function(t){switch(function(e,t){return(e=t.exec(e))?e[0]:e}(t,/(::plac\w+|:read-\w+)/)){case":read-only":case":read-write":return G([x(s(t,/:(read-\w+)/,":-moz-$1"),e,"")],n);case"::placeholder":return G([x(s(t,/:(plac\w+)/,":-webkit-input-$1"),e,""),x(s(t,/:(plac\w+)/,":-moz-$1"),e,""),x(s(t,/:(plac\w+)/,z+"input-$1"),e,"")],n)}return""}))}}],re=function(e){var t=e.key;if("css"===t){var r=document.querySelectorAll("style[data-emotion]:not([data-s])");Array.prototype.forEach.call(r,(function(e){-1!==e.getAttribute("data-emotion").indexOf(" ")&&(document.head.appendChild(e),e.setAttribute("data-s",""))}))}var a=e.stylisPlugins||te;var o,c,s={},i=[];o=e.container||document.head,Array.prototype.forEach.call(document.querySelectorAll('style[data-emotion^="'+t+' "]'),(function(e){for(var t=e.getAttribute("data-emotion").split(" "),r=1;r<t.length;r++)s[t[r]]=!0;i.push(e)}));var u,f,l=[B,(f=function(e){u.insert(e)},function(e){e.root||(e=e.return)&&f(e)})],d=function(e){var t=p(e);return function(r,n,a,o){for(var c="",s=0;s<t;s++)c+=e[s](r,n,a,o)||"";return c}}([Q,ee].concat(a,l));c=function(e,t,r,n){u=r,G(q(e?e+"{"+t.styles+"}":t.styles),d),n&&(y.inserted[t.name]=!0)};var y={key:t,sheet:new n.m({key:t,container:o,nonce:e.nonce,speedy:e.speedy,prepend:e.prepend}),nonce:e.nonce,inserted:s,registered:{},insert:c};return y.sheet.hydrate(i),y}},4759:function(e,t,r){"use strict";r.d(t,{E:function(){return d},T:function(){return f},c:function(){return p},h:function(){return s},w:function(){return u}});var n=r(7294),a=r(1859),o=r(444),c=r(9984),s=Object.prototype.hasOwnProperty,i=(0,n.createContext)("undefined"!==typeof HTMLElement?(0,a.Z)({key:"css"}):null);i.Provider;var u=function(e){return(0,n.forwardRef)((function(t,r){var a=(0,n.useContext)(i);return e(t,a,r)}))},f=(0,n.createContext)({});var l="__EMOTION_TYPE_PLEASE_DO_NOT_USE__",p=function(e,t){var r={};for(var n in t)s.call(t,n)&&(r[n]=t[n]);return r[l]=e,r},d=u((function(e,t,r){var a=e.css;"string"===typeof a&&void 0!==t.registered[a]&&(a=t.registered[a]);var i=e[l],u=[a],p="";"string"===typeof e.className?p=(0,o.f)(t.registered,u,e.className):null!=e.className&&(p=e.className+" ");var d=(0,c.O)(u,void 0,(0,n.useContext)(f));(0,o.M)(t,d,"string"===typeof i);p+=t.key+"-"+d.name;var y={};for(var h in e)s.call(e,h)&&"css"!==h&&h!==l&&(y[h]=e[h]);return y.ref=r,y.className=p,(0,n.createElement)(i,y)}))},917:function(e,t,r){"use strict";r.d(t,{xB:function(){return i},iv:function(){return u}});var n=r(7294),a=(r(1859),r(4759)),o=(r(8679),r(444)),c=r(9984),s=r(1526),i=(0,a.w)((function(e,t){var r=e.styles,i=(0,c.O)([r],void 0,(0,n.useContext)(a.T)),u=(0,n.useRef)();return(0,n.useLayoutEffect)((function(){var e=t.key+"-global",r=new s.m({key:e,nonce:t.sheet.nonce,container:t.sheet.container,speedy:t.sheet.isSpeedy}),n=!1,a=document.querySelector('style[data-emotion="'+e+" "+i.name+'"]');return t.sheet.tags.length&&(r.before=t.sheet.tags[0]),null!==a&&(n=!0,a.setAttribute("data-emotion",e),r.hydrate([a])),u.current=[r,n],function(){r.flush()}}),[t]),(0,n.useLayoutEffect)((function(){var e=u.current,r=e[0];if(e[1])e[1]=!1;else{if(void 0!==i.next&&(0,o.M)(t,i.next,!0),r.tags.length){var n=r.tags[r.tags.length-1].nextElementSibling;r.before=n,r.flush()}t.insert("",i,r,!1)}}),[t,i.name]),null}));function u(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];return(0,c.O)(t)}},5944:function(e,t,r){"use strict";r.d(t,{tZ:function(){return o},BX:function(){return c}});r(7294),r(1859);var n=r(4759),a=(r(8679),r(9984),r(5893));a.Fragment;function o(e,t,r){return n.h.call(t,"css")?(0,a.jsx)(n.E,(0,n.c)(e,t),r):(0,a.jsx)(e,t,r)}function c(e,t,r){return n.h.call(t,"css")?(0,a.jsxs)(n.E,(0,n.c)(e,t),r):(0,a.jsxs)(e,t,r)}},9984:function(e,t,r){"use strict";r.d(t,{O:function(){return y}});var n=function(e){for(var t,r=0,n=0,a=e.length;a>=4;++n,a-=4)t=1540483477*(65535&(t=255&e.charCodeAt(n)|(255&e.charCodeAt(++n))<<8|(255&e.charCodeAt(++n))<<16|(255&e.charCodeAt(++n))<<24))+(59797*(t>>>16)<<16),r=1540483477*(65535&(t^=t>>>24))+(59797*(t>>>16)<<16)^1540483477*(65535&r)+(59797*(r>>>16)<<16);switch(a){case 3:r^=(255&e.charCodeAt(n+2))<<16;case 2:r^=(255&e.charCodeAt(n+1))<<8;case 1:r=1540483477*(65535&(r^=255&e.charCodeAt(n)))+(59797*(r>>>16)<<16)}return(((r=1540483477*(65535&(r^=r>>>13))+(59797*(r>>>16)<<16))^r>>>15)>>>0).toString(36)},a={animationIterationCount:1,borderImageOutset:1,borderImageSlice:1,borderImageWidth:1,boxFlex:1,boxFlexGroup:1,boxOrdinalGroup:1,columnCount:1,columns:1,flex:1,flexGrow:1,flexPositive:1,flexShrink:1,flexNegative:1,flexOrder:1,gridRow:1,gridRowEnd:1,gridRowSpan:1,gridRowStart:1,gridColumn:1,gridColumnEnd:1,gridColumnSpan:1,gridColumnStart:1,msGridRow:1,msGridRowSpan:1,msGridColumn:1,msGridColumnSpan:1,fontWeight:1,lineHeight:1,opacity:1,order:1,orphans:1,tabSize:1,widows:1,zIndex:1,zoom:1,WebkitLineClamp:1,fillOpacity:1,floodOpacity:1,stopOpacity:1,strokeDasharray:1,strokeDashoffset:1,strokeMiterlimit:1,strokeOpacity:1,strokeWidth:1};var o=/[A-Z]|^ms/g,c=/_EMO_([^_]+?)_([^]*?)_EMO_/g,s=function(e){return 45===e.charCodeAt(1)},i=function(e){return null!=e&&"boolean"!==typeof e},u=function(e){var t=Object.create(null);return function(r){return void 0===t[r]&&(t[r]=e(r)),t[r]}}((function(e){return s(e)?e:e.replace(o,"-$&").toLowerCase()})),f=function(e,t){switch(e){case"animation":case"animationName":if("string"===typeof t)return t.replace(c,(function(e,t,r){return p={name:t,styles:r,next:p},t}))}return 1===a[e]||s(e)||"number"!==typeof t||0===t?t:t+"px"};function l(e,t,r){if(null==r)return"";if(void 0!==r.__emotion_styles)return r;switch(typeof r){case"boolean":return"";case"object":if(1===r.anim)return p={name:r.name,styles:r.styles,next:p},r.name;if(void 0!==r.styles){var n=r.next;if(void 0!==n)for(;void 0!==n;)p={name:n.name,styles:n.styles,next:p},n=n.next;return r.styles+";"}return function(e,t,r){var n="";if(Array.isArray(r))for(var a=0;a<r.length;a++)n+=l(e,t,r[a])+";";else for(var o in r){var c=r[o];if("object"!==typeof c)null!=t&&void 0!==t[c]?n+=o+"{"+t[c]+"}":i(c)&&(n+=u(o)+":"+f(o,c)+";");else if(!Array.isArray(c)||"string"!==typeof c[0]||null!=t&&void 0!==t[c[0]]){var s=l(e,t,c);switch(o){case"animation":case"animationName":n+=u(o)+":"+s+";";break;default:n+=o+"{"+s+"}"}}else for(var p=0;p<c.length;p++)i(c[p])&&(n+=u(o)+":"+f(o,c[p])+";")}return n}(e,t,r);case"function":if(void 0!==e){var a=p,o=r(e);return p=a,l(e,t,o)}break;case"string":}if(null==t)return r;var c=t[r];return void 0!==c?c:r}var p,d=/label:\s*([^\s;\n{]+)\s*(;|$)/g;var y=function(e,t,r){if(1===e.length&&"object"===typeof e[0]&&null!==e[0]&&void 0!==e[0].styles)return e[0];var a=!0,o="";p=void 0;var c=e[0];null==c||void 0===c.raw?(a=!1,o+=l(r,t,c)):o+=c[0];for(var s=1;s<e.length;s++)o+=l(r,t,e[s]),a&&(o+=c[s]);d.lastIndex=0;for(var i,u="";null!==(i=d.exec(o));)u+="-"+i[1];return{name:n(o)+u,styles:o,next:p}}},1526:function(e,t,r){"use strict";r.d(t,{m:function(){return n}});var n=function(){function e(e){var t=this;this._insertTag=function(e){var r;r=0===t.tags.length?t.prepend?t.container.firstChild:t.before:t.tags[t.tags.length-1].nextSibling,t.container.insertBefore(e,r),t.tags.push(e)},this.isSpeedy=void 0===e.speedy||e.speedy,this.tags=[],this.ctr=0,this.nonce=e.nonce,this.key=e.key,this.container=e.container,this.prepend=e.prepend,this.before=null}var t=e.prototype;return t.hydrate=function(e){e.forEach(this._insertTag)},t.insert=function(e){this.ctr%(this.isSpeedy?65e3:1)===0&&this._insertTag(function(e){var t=document.createElement("style");return t.setAttribute("data-emotion",e.key),void 0!==e.nonce&&t.setAttribute("nonce",e.nonce),t.appendChild(document.createTextNode("")),t.setAttribute("data-s",""),t}(this));var t=this.tags[this.tags.length-1];if(this.isSpeedy){var r=function(e){if(e.sheet)return e.sheet;for(var t=0;t<document.styleSheets.length;t++)if(document.styleSheets[t].ownerNode===e)return document.styleSheets[t]}(t);try{r.insertRule(e,r.cssRules.length)}catch(n){0}}else t.appendChild(document.createTextNode(e));this.ctr++},t.flush=function(){this.tags.forEach((function(e){return e.parentNode&&e.parentNode.removeChild(e)})),this.tags=[],this.ctr=0},e}()},444:function(e,t,r){"use strict";r.d(t,{f:function(){return n},M:function(){return a}});function n(e,t,r){var n="";return r.split(" ").forEach((function(r){void 0!==e[r]?t.push(e[r]+";"):n+=r+" "})),n}var a=function(e,t,r){var n=e.key+"-"+t.name;if(!1===r&&void 0===e.registered[n]&&(e.registered[n]=t.styles),void 0===e.inserted[t.name]){var a=t;do{e.insert(t===a?"."+n:"",a,e.sheet,!0);a=a.next}while(void 0!==a)}}},8679:function(e,t,r){"use strict";var n=r(1296),a={childContextTypes:!0,contextType:!0,contextTypes:!0,defaultProps:!0,displayName:!0,getDefaultProps:!0,getDerivedStateFromError:!0,getDerivedStateFromProps:!0,mixins:!0,propTypes:!0,type:!0},o={name:!0,length:!0,prototype:!0,caller:!0,callee:!0,arguments:!0,arity:!0},c={$$typeof:!0,compare:!0,defaultProps:!0,displayName:!0,propTypes:!0,type:!0},s={};function i(e){return n.isMemo(e)?c:s[e.$$typeof]||a}s[n.ForwardRef]={$$typeof:!0,render:!0,defaultProps:!0,displayName:!0,propTypes:!0},s[n.Memo]=c;var u=Object.defineProperty,f=Object.getOwnPropertyNames,l=Object.getOwnPropertySymbols,p=Object.getOwnPropertyDescriptor,d=Object.getPrototypeOf,y=Object.prototype;e.exports=function e(t,r,n){if("string"!==typeof r){if(y){var a=d(r);a&&a!==y&&e(t,a,n)}var c=f(r);l&&(c=c.concat(l(r)));for(var s=i(t),h=i(r),m=0;m<c.length;++m){var v=c[m];if(!o[v]&&(!n||!n[v])&&(!h||!h[v])&&(!s||!s[v])){var g=p(r,v);try{u(t,v,g)}catch(b){}}}}return t}},6103:function(e,t){"use strict";var r="function"===typeof Symbol&&Symbol.for,n=r?Symbol.for("react.element"):60103,a=r?Symbol.for("react.portal"):60106,o=r?Symbol.for("react.fragment"):60107,c=r?Symbol.for("react.strict_mode"):60108,s=r?Symbol.for("react.profiler"):60114,i=r?Symbol.for("react.provider"):60109,u=r?Symbol.for("react.context"):60110,f=r?Symbol.for("react.async_mode"):60111,l=r?Symbol.for("react.concurrent_mode"):60111,p=r?Symbol.for("react.forward_ref"):60112,d=r?Symbol.for("react.suspense"):60113,y=r?Symbol.for("react.suspense_list"):60120,h=r?Symbol.for("react.memo"):60115,m=r?Symbol.for("react.lazy"):60116,v=r?Symbol.for("react.block"):60121,g=r?Symbol.for("react.fundamental"):60117,b=r?Symbol.for("react.responder"):60118,w=r?Symbol.for("react.scope"):60119;function x(e){if("object"===typeof e&&null!==e){var t=e.$$typeof;switch(t){case n:switch(e=e.type){case f:case l:case o:case s:case c:case d:return e;default:switch(e=e&&e.$$typeof){case u:case p:case m:case h:case i:return e;default:return t}}case a:return t}}}function $(e){return x(e)===l}t.AsyncMode=f,t.ConcurrentMode=l,t.ContextConsumer=u,t.ContextProvider=i,t.Element=n,t.ForwardRef=p,t.Fragment=o,t.Lazy=m,t.Memo=h,t.Portal=a,t.Profiler=s,t.StrictMode=c,t.Suspense=d,t.isAsyncMode=function(e){return $(e)||x(e)===f},t.isConcurrentMode=$,t.isContextConsumer=function(e){return x(e)===u},t.isContextProvider=function(e){return x(e)===i},t.isElement=function(e){return"object"===typeof e&&null!==e&&e.$$typeof===n},t.isForwardRef=function(e){return x(e)===p},t.isFragment=function(e){return x(e)===o},t.isLazy=function(e){return x(e)===m},t.isMemo=function(e){return x(e)===h},t.isPortal=function(e){return x(e)===a},t.isProfiler=function(e){return x(e)===s},t.isStrictMode=function(e){return x(e)===c},t.isSuspense=function(e){return x(e)===d},t.isValidElementType=function(e){return"string"===typeof e||"function"===typeof e||e===o||e===l||e===s||e===c||e===d||e===y||"object"===typeof e&&null!==e&&(e.$$typeof===m||e.$$typeof===h||e.$$typeof===i||e.$$typeof===u||e.$$typeof===p||e.$$typeof===g||e.$$typeof===b||e.$$typeof===w||e.$$typeof===v)},t.typeOf=x},1296:function(e,t,r){"use strict";e.exports=r(6103)},3894:function(e,t,r){"use strict";r.d(t,{KP:function(){return a},b8:function(){return o}});var n=r(7294);var a={name:"oorag9",styles:"html{background:black;}body{min-width:100vh;min-height:100vh;margin:0 auto;background:#eee;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Oxygen,Ubuntu,Cantarell,Fira Sans,Droid Sans,Helvetica Neue,sans-serif;font-size:15px;}a{color:inherit;text-decoration:none;}"},o={name:"qo0nov",styles:"display:flex;flex-direction:column;min-width:100vh;min-height:100vh;max-height:100vh;overflow:hidden"},c=(0,n.createContext)({});t.ZP=c},826:function(e,t,r){"use strict";function n(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}r.r(t),r.d(t,{default:function(){return h}});var a=r(917),o=r(3894);function c(e,t,r,n,a,o,c){try{var s=e[o](c),i=s.value}catch(u){return void r(u)}s.done?t(i):Promise.resolve(i).then(n,a)}var s=r(809),i=r.n(s),u=r(7294),f=function(){var e=(0,u.useState)(""),t=e[0],r=e[1],n=(0,u.useState)([]),a=n[0],o=n[1],s=function(e){r(e.newMessage),setTimeout(f,e.lasting)},f=function(){a.shift(),o(a),a.length>0?s(a[0]):r("")};return{message:t,planMessage:function(){var e,r=(e=i().mark((function e(r){return i().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:a.push(r),o(a),""==t&&s(a[0]);case 3:case"end":return e.stop()}}),e)})),function(){var t=this,r=arguments;return new Promise((function(n,a){var o=e.apply(t,r);function s(e){c(o,n,a,s,i,"next",e)}function i(e){c(o,n,a,s,i,"throw",e)}s(void 0)}))});return function(e){return r.apply(this,arguments)}}()}},l=function(){var e=f(),t=e.message,r=e.planMessage;return{style:{globalStyle:o.KP,pageS:o.b8},message:t,planMessage:r}},p=r(5944);function d(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function y(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?d(Object(r),!0).forEach((function(t){n(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):d(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var h=function(e){var t=e.Component,r=e.pageProps,n=l();return(0,p.BX)(o.ZP.Provider,{value:n,children:[(0,p.tZ)(a.xB,{styles:n.style.globalStyle}),(0,p.tZ)(t,y({},r))]})}},6363:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/_app",function(){return r(826)}])}},function(e){var t=function(t){return e(e.s=t)};e.O(0,[774,179],(function(){return t(6363),t(4651)}));var r=e.O();_N_E=r}]);
document.addEventListener('alpine:init',()=>{
 Alpine.store('theme',{dark:localStorage.getItem('theme')==='dark',toggle(){this.dark=!this.dark;localStorage.setItem('theme',this.dark?'dark':'light')}})
 Alpine.store('toasts',{items:[],push(message,type='success'){const id=Date.now();this.items.push({id,message,type});setTimeout(()=>this.items=this.items.filter(t=>t.id!==id),4000)}})
 Alpine.data('directory',()=>({query:'',grid:localStorage.getItem('grid')!=='false',loading:false}))
 Alpine.data('tabs',()=>({tab:'about'}))
 Alpine.data('bookingWizard',()=>({step:1,date:'',slot:'',visit:'',reason:'',get remaining(){return 300-this.reason.length},get canAdvance(){return !!(this.date&&this.slot&&this.visit)},init(){this.$watch('step',v=>sessionStorage.setItem('bookingStep',v));this.step=Number(sessionStorage.getItem('bookingStep')||1)}}))
 Alpine.data('management',()=>({status:'All',selected:[],openCancel:false,get filteredItems(){return this.status}}))
})
document.body?.addEventListener('toast',e=>Alpine.store('toasts').push(e.detail.message,e.detail.type))

import { CommonModule } from '@angular/common';
import { Component, OnInit, computed, signal } from '@angular/core';
import { ApiService } from './core/api.service';

interface Ticket { id:string; customer:string; device:string; service:string; status:string; priority:string; owner:string; due:string }

@Component({selector:'app-root',imports:[CommonModule],templateUrl:'./app.html',styleUrl:'./app.scss'})
export class App implements OnInit {
  menuOpen=signal(false); dark=signal(false); active=signal('Overview'); query=signal('');
  nav=[['Overview','⌂'],['Service tickets','◇'],['Customers','♙'],['Team','♧'],['Inventory','□'],['Invoices','▤'],['Reports','⌁']];
  tickets=signal<Ticket[]>([
    {id:'#OS-1048',customer:'Nadia Rahman',device:'MacBook Pro 14″',service:'Display replacement',status:'In progress',priority:'High',owner:'AR',due:'Today, 4:30 PM'},
    {id:'#OS-1047',customer:'Marcus Lee',device:'iPhone 15 Pro',service:'Battery diagnostics',status:'Awaiting parts',priority:'Medium',owner:'SK',due:'Tomorrow'},
    {id:'#OS-1046',customer:'Ayesha Khan',device:'Dell XPS 13',service:'System recovery',status:'Ready',priority:'Low',owner:'JM',due:'Sep 14'},
    {id:'#OS-1045',customer:'Daniel Cooper',device:'Samsung S24',service:'Camera module repair',status:'New',priority:'High',owner:'AR',due:'Sep 15'}
  ]);
  visible=computed(()=>{const q=this.query().toLowerCase().trim();return q?this.tickets().filter(t=>Object.values(t).some(v=>v.toLowerCase().includes(q))):this.tickets()});
  constructor(readonly api:ApiService){}
  ngOnInit(){this.api.connectDemo().subscribe({next:values=>this.tickets.set(values.map((t,index)=>({id:'#'+t.reference,customer:['Nadia Rahman','Marcus Lee','Ayesha Khan'][index]??'Customer',device:t.device,service:t.title,status:t.status.replaceAll('_',' ').replace(/^./,c=>c.toUpperCase()),priority:t.priority.replace(/^./,c=>c.toUpperCase()),owner:t.assigned_to?'AR':'—',due:t.due_date??'Not set'}))),error:()=>this.api.connected.set(false)})}
  search(e:Event){this.query.set((e.target as HTMLInputElement).value)}
  select(label:string){this.active.set(label);this.menuOpen.set(false)}
}

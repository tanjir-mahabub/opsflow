import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { forkJoin, switchMap, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ApiTicket { id:number; reference:string; customer_id:number; title:string; device:string; description:string; status:string; priority:string; due_date:string|null; assigned_to:number|null; estimated_cost:number; created_at:string }
export interface Customer { id:number; name:string; email:string; phone:string; company:string|null; created_at:string }
export interface InventoryItem { id:number; sku:string; name:string; category:string; quantity:number; reorder_level:number; unit_cost:number; low_stock:boolean }
export interface Invoice { id:number; number:string; customer_id:number; ticket_id:number|null; subtotal:number; tax:number; discount:number; paid:number; due_date:string|null; status:string; total:number; balance:number }
export interface TeamMember { id:number; name:string; email:string; role:string }
export interface Stats { active_tickets:number; completed_tickets:number; customers:number; low_stock_items:number; revenue:number; outstanding:number }
interface LoginResponse { access_token:string; user:TeamMember }

@Injectable({providedIn:'root'})
export class ApiService {
  private readonly baseUrl=environment.apiUrl;
  private token=sessionStorage.getItem('opsflow_token')??'';
  readonly user=signal<TeamMember|null>(null);
  readonly connected=signal(false);
  constructor(private readonly http:HttpClient){}
  connectDemo(){return this.http.post<LoginResponse>(`${this.baseUrl}/auth/login`,{email:'admin@opsflow.dev',password:'OpsFlow123!'}).pipe(tap(response=>{this.token=response.access_token;sessionStorage.setItem('opsflow_token',this.token);this.user.set(response.user);this.connected.set(true)}),switchMap(()=>this.loadWorkspace()))}
  loadWorkspace(){return forkJoin({tickets:this.get<ApiTicket[]>('/tickets'),customers:this.get<Customer[]>('/customers'),inventory:this.get<InventoryItem[]>('/inventory'),invoices:this.get<Invoice[]>('/invoices'),team:this.get<TeamMember[]>('/team'),stats:this.get<Stats>('/dashboard/stats')})}
  get<T>(path:string){return this.http.get<T>(`${this.baseUrl}${path}`,{headers:this.headers()})}
  post<T>(path:string,body:unknown){return this.http.post<T>(`${this.baseUrl}${path}`,body,{headers:this.headers()})}
  patch<T>(path:string,body:unknown={}){return this.http.patch<T>(`${this.baseUrl}${path}`,body,{headers:this.headers()})}
  delete(path:string){return this.http.delete<void>(`${this.baseUrl}${path}`,{headers:this.headers()})}
  private headers(){return new HttpHeaders({Authorization:`Bearer ${this.token}`})}
}

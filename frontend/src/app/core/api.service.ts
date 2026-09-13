import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable, switchMap, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface ApiTicket {
  id:number; reference:string; title:string; device:string; status:string; priority:string;
  due_date:string|null; assigned_to:number|null; estimated_cost:number;
}
interface LoginResponse { access_token:string; user:{id:number;name:string;email:string;role:string} }

@Injectable({providedIn:'root'})
export class ApiService {
  private readonly baseUrl=environment.apiUrl;
  private token='';
  readonly user=signal<LoginResponse['user']|null>(null);
  readonly connected=signal(false);
  constructor(private readonly http:HttpClient){}
  connectDemo():Observable<ApiTicket[]> {
    return this.http.post<LoginResponse>(`${this.baseUrl}/auth/login`,{email:'admin@opsflow.dev',password:'OpsFlow123!'}).pipe(
      tap(response=>{this.token=response.access_token;this.user.set(response.user);this.connected.set(true)}),
      switchMap(()=>this.http.get<ApiTicket[]>(`${this.baseUrl}/tickets`,{headers:this.headers()}))
    );
  }
  private headers(){return new HttpHeaders({Authorization:`Bearer ${this.token}`})}
}

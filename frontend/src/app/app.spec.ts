import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
describe('App',()=>{beforeEach(async()=>TestBed.configureTestingModule({imports:[App],providers:[provideHttpClient(),provideHttpClientTesting()]}).compileComponents());it('renders the secure OpsFlow login',()=>{const f=TestBed.createComponent(App);f.detectChanges();expect(f.componentInstance).toBeTruthy();expect((f.nativeElement as HTMLElement).textContent).toContain('OpsFlow');expect((f.nativeElement as HTMLElement).textContent).toContain('Explore live demo')})});

import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
describe('App',()=>{beforeEach(async()=>TestBed.configureTestingModule({imports:[App],providers:[provideHttpClient(),provideHttpClientTesting()]}).compileComponents());it('creates OpsFlow',()=>{const f=TestBed.createComponent(App);expect(f.componentInstance).toBeTruthy();expect((f.nativeElement as HTMLElement).textContent).toContain('OpsFlow')})});

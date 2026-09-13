import { TestBed } from '@angular/core/testing';
import { App } from './app';
describe('App',()=>{beforeEach(async()=>TestBed.configureTestingModule({imports:[App]}).compileComponents());it('creates OpsFlow',()=>{const f=TestBed.createComponent(App);expect(f.componentInstance).toBeTruthy();expect((f.nativeElement as HTMLElement).textContent).toContain('OpsFlow')})});

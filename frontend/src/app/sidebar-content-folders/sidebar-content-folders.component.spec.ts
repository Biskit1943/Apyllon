import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarContentFoldersComponent } from './sidebar-content-folders.component';

describe('SidebarContentFoldersComponent', () => {
  let component: SidebarContentFoldersComponent;
  let fixture: ComponentFixture<SidebarContentFoldersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidebarContentFoldersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarContentFoldersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

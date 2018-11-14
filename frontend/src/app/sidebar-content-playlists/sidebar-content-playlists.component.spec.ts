import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarContentPlaylistsComponent } from './sidebar-content-playlists.component';

describe('SidebarContentPlaylistsComponent', () => {
  let component: SidebarContentPlaylistsComponent;
  let fixture: ComponentFixture<SidebarContentPlaylistsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidebarContentPlaylistsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarContentPlaylistsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

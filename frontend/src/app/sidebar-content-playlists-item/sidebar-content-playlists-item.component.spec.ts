import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidebarContentPlaylistsItemComponent } from './sidebar-content-playlists-item.component';

describe('SidebarContentPlaylistsItemComponent', () => {
  let component: SidebarContentPlaylistsItemComponent;
  let fixture: ComponentFixture<SidebarContentPlaylistsItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidebarContentPlaylistsItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidebarContentPlaylistsItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-sidebar-content-playlists',
  templateUrl: './sidebar-content-playlists.component.html',
  styleUrls: ['./sidebar-content-playlists.component.css']
})
export class SidebarContentPlaylistsComponent implements OnInit {

  Playlists = ['Sport', 'Chillen', 'Wandern', 'Arbeiten', 'Glücklich', 'Traurig', 'Wütend'];

  constructor() {

  }

  ngOnInit() {
  }

}

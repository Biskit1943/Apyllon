import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-sidebar-content-playlists-item',
  templateUrl: './sidebar-content-playlists-item.component.html',
  styleUrls: ['./sidebar-content-playlists-item.component.css']
})
export class SidebarContentPlaylistsItemComponent implements OnInit {

  @Input() playlist: String;

  constructor() {
  }

  openPlaylist() {
    console.log('Open Playlist');
  }

  ngOnInit() {
  }

}

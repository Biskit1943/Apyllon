import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SidebarContentFoldersComponent } from './sidebar-content-folders/sidebar-content-folders.component';
import { SidebarContentPlaylistsComponent } from './sidebar-content-playlists/sidebar-content-playlists.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { SidebarContentPlaylistsItemComponent } from './sidebar-content-playlists-item/sidebar-content-playlists-item.component';

import { ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
// used to create fake backend
import { ErrorInterceptor, JwtInterceptor } from './_helpers';
import { routing } from './app.routing';

import { AlertComponent } from './_directives';
import { AuthGuard } from './_guards';
import { AlertService, AuthenticationService, PlayerService, UploadService, UserService } from './_services';
import { HomeComponent } from './home';
import { LoginComponent } from './login';
import { RegisterComponent } from './register';
import { LayoutModule } from '@angular/cdk/layout';
import {
  MatButtonModule,
  MatDialogModule,
  MatIconModule,
  MatListModule,
  MatProgressBar,
  MatSidenavModule,
  MatToolbarModule
} from '@angular/material';
import { MainSidebarComponent } from './main-sidebar/main-sidebar.component';
import { PlayerComponent } from './player/player.component';
import { PasswordComponent } from './password';
import { UploadComponent } from './upload/upload.component';
import { DialogComponent } from './upload/dialog/dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    SidebarContentFoldersComponent,
    SidebarContentPlaylistsComponent,
    SidebarContentPlaylistsItemComponent,
    AlertComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    MainSidebarComponent,
    PlayerComponent,
    MatProgressBar,
    PasswordComponent,
    UploadComponent,
    DialogComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    HttpClientModule,
    routing,
    LayoutModule,
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatDialogModule
  ],
  providers: [
    AuthGuard,
    AlertService,
    AuthenticationService,
    UserService,
    PlayerService,
    UploadService,
    {provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
  ],
  entryComponents: [DialogComponent],
  bootstrap: [AppComponent]
})
export class AppModule {
}

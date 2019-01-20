import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AlertService, AuthenticationService } from '../_services';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-password',
  templateUrl: './password.component.html',
  styleUrls: ['./password.component.css']
})

export class PasswordComponent implements OnInit {
  passwordForm: FormGroup;
  loading = false;
  submitted = false;
  returnUrl: string;
  user: String = '';


  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenticationService: AuthenticationService,
    private activatedRoute: ActivatedRoute,
    private alertService: AlertService) {
  }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe(params => {
      this.user = params['user'];
    });
    this.passwordForm = this.formBuilder.group({
      currentPassword: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(6)]]
    });

    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.passwordForm.controls;
  }
  get v() {
    return this.passwordForm.value;
  }

  onSubmit() {
    this.submitted = true;

    // stop here if form is invalid
    if (this.passwordForm.invalid) {
      return;
    }
    if (this.v.password !== this.v.confirmPassword) {
      this.alertService.error('New Passwords do not match', true);
      return;
    }

    this.loading = true;
    this.authenticationService.changePassword(this.user, this.v.currentPassword, this.v.password)
      .pipe(first())
      .subscribe(
        data => {
          this.alertService.success('Successfully changed password');
          this.router.navigate([this.returnUrl]);
        },
        error => {
          this.alertService.error(error, true);
          this.loading = false;
        });
  }
}

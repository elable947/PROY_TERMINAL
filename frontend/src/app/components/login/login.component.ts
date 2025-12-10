import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, RouterModule],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {
    private fb = inject(FormBuilder);
    private authService = inject(AuthService);
    private router = inject(Router);

    loginForm: FormGroup = this.fb.group({
        username: ['', Validators.required],
        password: ['', Validators.required]
    });

    errorMessage: string = '';
    isLoading: boolean = false;

    onSubmit() {
        if (this.loginForm.invalid) return;

        this.isLoading = true;
        this.errorMessage = '';

        this.authService.login(this.loginForm.value).subscribe({
            next: (res) => {
                this.isLoading = false;
                console.log('Login success', res);
                this.redirectUser(res.user.idTipoUsuario);
            },
            error: (err) => {
                this.isLoading = false;
                console.error('Login error', err);
                this.errorMessage = err.error?.error || 'Error al iniciar sesión';
            }
        });
    }

    redirectUser(roleId: number) {
        switch (roleId) {
            case 3: // Administrador
                this.router.navigate(['/admin']);
                break;
            case 2: // Empresa
                this.router.navigate(['/company']);
                break;
            case 4: // Conductor
                this.router.navigate(['/driver']);
                break;
            default: // Pasajero (1) and others
                this.router.navigate(['/']);
                break;
        }
    }
}

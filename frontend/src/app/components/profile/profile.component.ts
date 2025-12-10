import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { DataService } from '../../services/data.service';

@Component({
    selector: 'app-profile',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule],
    templateUrl: './profile.component.html',
    styleUrl: './profile.component.css'
})
export class ProfileComponent implements OnInit {
    private authService = inject(AuthService);
    private dataService = inject(DataService);
    private fb = inject(FormBuilder);

    paises: any[] = [];

    profileForm: FormGroup = this.fb.group({
        idUsuario: [''], // Hidden
        nombre_usuario: ['', Validators.required],
        apPaterno: ['', Validators.required],
        apMaterno: ['', Validators.required],
        correo: ['', [Validators.required, Validators.email]],
        telefono: ['', Validators.required],
        edad: ['', [Validators.required, Validators.min(18)]],
        dni: ['', [Validators.minLength(8)]],
        idPais: ['', Validators.required]
    });

    successMessage: string = '';
    errorMessage: string = '';

    ngOnInit() {
        // Load Paises
        this.dataService.getPaises().subscribe(data => this.paises = data);

        // Load current user data
        this.authService.currentUser$.subscribe(user => {
            if (user) {
                // Ensure idPais is set, default to 135 (Peru) if missing
                const userData = { ...user, idPais: user.idPais || 135 };
                this.profileForm.patchValue(userData);
            }
        });
    }

    onSubmit() {
        if (this.profileForm.invalid) return;

        this.authService.updateProfile(this.profileForm.value).subscribe({
            next: () => {
                this.successMessage = 'Perfil actualizado correctamente';
                this.errorMessage = '';
                setTimeout(() => this.successMessage = '', 3000);
            },
            error: err => {
                this.errorMessage = err.error?.error || 'Error al actualizar';
                this.successMessage = '';
            }
        });
    }

    goBack() {
        window.history.back();
    }

    getInitials(): string {
        const nombre = this.profileForm.get('nombre_usuario')?.value || '';
        return nombre.substring(0, 2).toUpperCase();
    }
}

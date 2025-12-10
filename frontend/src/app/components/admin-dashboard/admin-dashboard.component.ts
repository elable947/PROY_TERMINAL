import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin.service';
import { DataService } from '../../services/data.service';

@Component({
    selector: 'app-admin-dashboard',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, FormsModule],
    templateUrl: './admin-dashboard.component.html',
    styleUrl: './admin-dashboard.component.css'
})
export class AdminDashboardComponent implements OnInit {
    private adminService = inject(AdminService);
    private dataService = inject(DataService);
    private fb = inject(FormBuilder);

    activeTab: 'companies' | 'assign' = 'companies';

    // Data
    empresas: any[] = [];
    searchDni: string = '';
    searchedUser: any = null;

    // Forms
    companyForm: FormGroup = this.fb.group({
        nombreEmpresa: ['', Validators.required],
        ruc: ['', [Validators.required, Validators.minLength(11)]],
        razonSocial: [''],
        telefonoEmpresa: ['']
    });

    assignForm: FormGroup = this.fb.group({
        idUsuario: ['', Validators.required],
        idEmpresa: ['', Validators.required]
    });

    successMessage: string = '';
    errorMessage: string = '';

    // Modal state
    showDetailsModal = false;
    selectedCompanyDetails: any = null;

    ngOnInit(): void {
        this.loadEmpresas();
    }

    loadEmpresas() {
        this.dataService.getEmpresas().subscribe(data => {
            this.empresas = data;
        });
    }

    viewCompanyDetails(id: number) {
        this.adminService.getCompanyDetails(id).subscribe({
            next: (data) => {
                this.selectedCompanyDetails = data;
                this.showDetailsModal = true;
            },
            error: (err) => {
                console.error(err);
                this.errorMessage = 'Error al cargar detalles de la empresa';
            }
        });
    }

    closeModal() {
        this.showDetailsModal = false;
        this.selectedCompanyDetails = null;
    }

    createCompany() {
        if (this.companyForm.invalid) return;

        this.adminService.createCompany(this.companyForm.value).subscribe({
            next: () => {
                this.successMessage = 'Empresa creada con éxito.';
                this.companyForm.reset();
                this.loadEmpresas();
                setTimeout(() => this.successMessage = '', 3000);
            },
            error: err => this.errorMessage = 'Error: ' + err.error?.error
        });
    }

    assignCompany() {
        if (this.assignForm.invalid) return;
        const { idUsuario, idEmpresa } = this.assignForm.value;

        this.adminService.assignCompany(idUsuario, idEmpresa).subscribe({
            next: () => {
                this.successMessage = 'Asignación correcta.';
                this.assignForm.reset();
                this.searchedUser = null;
                setTimeout(() => this.successMessage = '', 3000);
            },
            error: err => this.errorMessage = 'Error: ' + err.error?.error
        });
    }

    searchUser() {
        if (!this.searchDni) return;
        this.adminService.searchUserByDni(this.searchDni).subscribe({
            next: user => {
                this.searchedUser = user;
                this.assignForm.patchValue({ idUsuario: user.idUsuario });
                this.errorMessage = '';
            },
            error: () => {
                this.searchedUser = null;
                this.errorMessage = 'Usuario no encontrado con ese DNI';
            }
        });
    }

    setActiveTab(tab: 'companies' | 'assign') {
        this.activeTab = tab;
        this.errorMessage = '';
        this.successMessage = '';
    }
}

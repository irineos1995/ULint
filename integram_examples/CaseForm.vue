<template>
    <div class="md-layout">
      <div class="md-layout-item">
        <simple-wizard :vertical="window.width <= 991" ref="simple-wizard" v-on:tab-change="tabChange">
          <template slot="header">
            <h3 v-if="debug"> {{ currentCase }} </h3>
            <h3 v-if="currentCase" class="title">
              {{currentCase.detailed_label}} 
              <br/> 
              <span v-if="currentCase.selection_date"><b>MedCo Selection Date:</b> {{currentCase.selection_date | changeDateFilter}}<br/></span> 
              <b>Case Creation Date:</b> {{currentCase.date_created | changeDateFilter}}
              <p style="text-align: right;padding-bottom: 0px !important">Case Status: <b>{{ currentCase.status }}</b></p>
            </h3>
            <h3 v-else class="title">Adding new case</h3>            
          </template>

          <wizard-tab :label="'claimant'" ref="tab_claimant" :before-change="() => validateStep('claimant')">
            <template slot="label">
              <span class="wizard-span-title">
                Claimant
              </span>
            </template>
            <claimant-details ref="claimant" @on-validated="onStepValidated" v-bind:read-only="this.$route.params.readOnly" v-bind:claimant-data="currentCase ? currentCase.claimant : getEmptyCaseObject().claimant"></claimant-details>
          </wizard-tab>

          <wizard-tab :label="'instructing_party'" ref="tab_instructing_party" :before-change="() => validateStep('instructing_party')">
            <template slot="label">
              <span class="wizard-span-title">
                Instructing Party
              </span>
            </template>
            <instructing-party-details ref="instructing_party" @on-validated="onStepValidated" v-bind:read-only="this.$route.params.readOnly" v-bind:instructing-party-data="currentCase ? currentCase.instructing_party: getEmptyCaseObject().instructing_party"></instructing-party-details>
          </wizard-tab>

          <wizard-tab :label="'instructions'" ref="tab_instructions" :before-change="() => validateStep('instructions')">
            <template slot="label">
              <span class="wizard-span-title">
                Special Instructions
              </span>
            </template>
            <instructions ref="instructions" @on-validated="onStepValidated" v-bind:read-only="this.$route.params.readOnly" v-bind:instructions-data="currentCase ? currentCase.instructions : getEmptyCaseObject().instructions"></instructions>
          </wizard-tab>

          <wizard-tab :label="'accident'" ref="tab_accident" :before-change="() => validateStep('accident')">
            <template slot="label">
              <span class="wizard-span-title">
                Accident
              </span>
            </template>
            <accident-details ref="accident" @on-validated="onStepValidated" v-bind:read-only="this.$route.params.readOnly" v-bind:accident-data="currentCase ? currentCase.accident : getEmptyCaseObject().accident"></accident-details>
          </wizard-tab>

          <wizard-tab :label="'insurance'" ref="tab_insurance" :before-change="() => validateStep('insurance')">
            <template slot="label">
              <span class="wizard-span-title">
                Insurance
              </span>
            </template>
            <insurance-details ref="insurance" v-bind:read-only="this.$route.params.readOnly" v-bind:insurance-data="currentCase ? currentCase.insurance : getEmptyCaseObject().insurance"></insurance-details>
          </wizard-tab>

          <wizard-tab :label="'records'" ref="tab_records" v-if="$route.params.id">
            <template slot="label">
              <span class="wizard-span-title">
                Records
              </span>
            </template>
            <div class="md-card" v-if="currentCase.id">
              <records v-bind:focus="focus" @on-validated="onStepValidated" v-bind:model="model" v-bind:id="currentCase.id" v-bind:attachment-types="AttachmentTypes" v-bind:require-expiry-date="requireExpiryDate"></records>
            </div>
          </wizard-tab>

          <wizard-tab :label="'appointments'" ref="tab_appointments" v-if="currentCase">
            <template slot="label">
              <span class="wizard-span-title">
                Booked
                <br>
                Appointments
              </span>
            </template>
            <appointments ref="appointments" @on-validated="onStepValidated" v-bind:appointments-data="currentCase.appointments"></appointments>
          </wizard-tab>

          <wizard-tab :label="'changelog'" ref="tab_changelog" v-if="currentCase &&  currentCase.changelogs">
            <template slot="label">
              <span class="wizard-span-title">
                Case Log
              </span>
            </template>
            <changelog ref="changelog" @on-validated="onStepValidated" v-bind:changelog-data="currentCase.changelogs"></changelog>
          </wizard-tab>

          <wizard-tab :label="'accounts'" ref="tab_accounts" v-if="$route.params.id">
            <template slot="label">
              <span class="wizard-span-title">
                Accounts
              </span>
            </template>
            <accounts ref="accounts" @on-validated="onStepValidated" v-bind:accounts-data="currentCase ? currentCase.accounts : getEmptyCaseObject().accounts"></accounts>
          </wizard-tab>

          <wizard-tab :label="'complaints'" ref="tab_complaints" v-if="$route.params.id">
            <template slot="label">
              <span class="wizard-span-title">
                Complaints
              </span>
            </template>
            <complaints ref="complaints" @on-validated="onStepValidated" v-bind:complaints-data="currentCase ? currentCase.complaints : getEmptyCaseObject().complaints"></complaints>
          </wizard-tab>

          <wizard-tab :label="'data_security'" ref="tab_data_security" v-if="$route.params.id">
            <template slot="label">
              <span class="wizard-span-title">
                Data
                <br>
                Security
              </span>
            </template>
            <data-security ref="data_security" @on-validated="onStepValidated" v-bind:data-security-data="currentCase ? currentCase.data_security : getEmptyCaseObject().data_security"></data-security>
          </wizard-tab>

          <wizard-tab :label="'attachments'" ref="tab_attachments" v-if="currentCase.id" :before-change="() => validateStep('attachments')">
            <template slot="label">
              <span class="wizard-span-title">
                All
                <br>
                Attachments
              </span>
            </template>
            <attachments ref="attachments" v-bind:id="currentCase.id" @on-validated-last="wizardComplete"></attachments>
          </wizard-tab>

        </simple-wizard>
        <div class="md-card" v-if="currentCase.id && should_display_attachments_component">
          <integra-attachment v-bind:focus="focus" v-bind:model="model" v-bind:id="currentCase.id" v-bind:attachment-types="AttachmentTypes" v-bind:require-expiry-date="requireExpiryDate"></integra-attachment>
        </div>
        <div class="md-card" v-if="currentCase.id && should_display_requests_component">
          <case-requests></case-requests>
        </div>
      </div>
    </div>
</template>
<script>
  import IntegraAttachment from "../Attachment/IntegraAttachment";
  import Records from "./Records.vue";
  import { mapActions } from 'vuex'
  import { mapGetters } from 'vuex'
  import InstructingPartyDetails from "./InstructingPartyDetails.vue"
  import AgencyDetails from "./AgencyDetails.vue"
  import ClaimantDetails from "./ClaimantDetails.vue"
  import AccidentDetails from "./AccidentDetails.vue"
  import InsuranceDetails from "./InsuranceDetails.vue"
  import Instructions from "./Instructions.vue"
  import Appointments from "./Appointments.vue"
  import Accounts from "./Accounts.vue"
  import Complaints from "./Complaints.vue"
  import DataSecurity from "./DataSecurity.vue"
  import Changelog from "./Changelog.vue"
  import Attachments from "./Attachments.vue"
  import CaseRequests from "../Requests/RequestsOnCase.vue"



  import Swal from "sweetalert2"
  import {SimpleWizard, WizardTab} from "vue-material-dashboard-pro/src/components"

  import moment from 'moment';
  
  export default {
    filters: {
    changeDateFilter:
      function (value) {
        var date = moment(value).format('DD/MM/YYYY')
        if (date === 'Invalid date'){
            return 'N/A'
        }else{
            return date
        }
      },
    },
    data() {
      return {
        window: {
          width: 0,
          height: 0
        },
        ClaimantAttachmentTypes : ['Proof of ID', 'Form of authority'],
        AppointmentsAttachmentTypes: ["appointment","report","scan", "prescription"],
        ChangelogAttachmentTypes: ['instruction letter', 'picture', 'addendum', "appointment","report","scan", "prescription", "insurance", "letter", "receipt"],
        AttachmentsAttachmentTypes: ['instruction letter', 'picture', 'addendum', "appointment","report","scan", "prescription", "insurance", "letter", "receipt"],
        RecordsAttachmentTypes: ['GP records', 'Hospital records', 'Imaging records', 'Engineer records', 'GP medical report other accident Previous reports records', 'GP medical report index accident Previous reports records', 'Orthopaedic medical report Previous reports records', 'Psychologist medical report Previous reports records', 'Other medical report Previous reports records', 'Psychological records', 'Dental records', 'Physiotherapy records', 'Chiropractor records', 'Osteopath records', 'Images', 'Miscellaneous records', 'AskCue search'],
        AccountsAttachmentTypes: [''],
        InstructingPartyAttachmentTypes : ['GP Instruction letter', 'Orthopaedic Instruction letter', 'Physiotherapy Instruction letter', 'Imaging Instruction letter', 'Psychological Instruction letter', 'Specialist Instruction letter'],
        AccidentAttachmentTypes: [''],
        InstructionsAttachmentTypes: [''],
        InsuranceAttachmentTypes: [''],
        AttachmentTypes : ['Proof of ID', 'Form of authority'],
        model: "Case",
        wizardModel: null,
        tabs_checked_by_default: ['tab_changelog', 'tab_appointments', 'tab_medical_reports', 'tab_accounts', 'tab_attachments', 'tab_records'],
        focus: ['Proof of ID', 'Form of authority'], //put this here as it is the first tab and there is not tab-change when initially loading a case
        should_display_attachments_component: true,
        should_display_requests_component: false,
        requireExpiryDate: false
      }
    },
    props: ['debug',
            ],
    components: {
      IntegraAttachment,
      Records,
      InstructingPartyDetails,
      AgencyDetails,
      ClaimantDetails,
      AccidentDetails,
      Instructions,
      InsuranceDetails,
      Appointments,
      Accounts,
      Complaints,
      DataSecurity,
      Changelog,
      Attachments,
      SimpleWizard,
      CaseRequests,
      WizardTab
    },
    methods: {
      handleResize() {
        this.window.width = window.innerWidth;
        this.window.height = window.innerHeight;
      },
      getEmptyCaseObject() {
        console.log(" >> getEmptyCaseObject <<" )
        return {
          label: null,
          selection_date: null,
          date_created: null,
          accounts: {
            payments: [],
            invoices: []
          },
          complaints: [],
          data_security: [],
          instructing_party: {
            instruction_received_at: null,
            name: null,
            medco_id: null,
            po_number: null,
            instruction_party_reference: null,
            type: null,
            records_required: null,
            file_handler: null,
            file_handlers: []
          },
          agency: {
            name: null,
            agency_reference: null,
            file_handler: null,
            file_handlers: []
          },
          claimant: {
            title: null,
            first_name: null,
            last_name: null,
            gender: null,
            date_of_birth: null,
            postcode: null,
            address1: null,
            address2: null,
            address3: null,
            mobile1: null,
            mobile2: null,
            telephone1: null,
            telephone2: null,
            email: null,
            marital_status: null,
            occupation: null,
            litigation_friend: null,
            addresses: []
          },
          accident: {
            date: null,
            type: null,
            description: null,
            injuries: null
          },
          instructions: {
            instructions: null,
            recommended_appointment_range_start: null,
            recommended_appointment_range_end: null,
            recommended_appointment_range_suggested_by: null,
            venue_parking: null,
            venue_disable_access: null,
            venue_lift_access: null,
            venue_child_friendly: null
          },
          products: [],
          insurance: {
            company: null,
            postcode: null,
            address1: null,
            address2: null,
            address3: null,
            telephone: null,
            facsimile: null,
            co_name: null,
            third_party_name: null,
            file_handler: null,
            direct_telephone: null,
            email: null
          },
          appointments: [],
          longlat: null
        }
      },
      ...mapActions([
        'setCurrentCase',
        'setCurrentCaseLabel',
        'refreshCurrentCase'
      ]),
      validateStep(ref) {
        return this.$refs[ref].validate()
      },
      onStepValidated(validated, model) {
        this.wizardModel = {...this.wizardModel, ...model}
        this.checkpointSave()
        console.log('checkpoint save')
      },
      createDummyCase(){
        this.$http
          .create({headers: { 'Content-Type': 'application/json'}})
          .post(this.url__case_create, this.currentCase )
          .then(response => {
                console.log(response)
                this.$http
                  .get(this.url__case_details+response.data.id+'/' )
                  .then(response => {
                    this.setCurrentCase(response.data)
                    this.refreshCurrentCase()
                    this.$router.push('/case/edit/'+response.data.id+'/')
                  })
                  .catch(function(error) {
                    console.error(error.response)
                    throw error
                  });
            })
          .catch(function(r) {
            if(r.response && r.response.data){
              var error_message = ''
              if ( typeof(r.response.data) === 'string' ){
                r.response.data.split('\n').splice(0,2)
                r.response.data.split('\n').splice(0,2).forEach(element => {
                  error_message += element+'</>'
                });
              } else if(typeof(r.response.data) === 'object'){
                for (var prop in r.response.data) {
                // error_message += '</br>'+prop+': '+r.response.data[prop][0]
                error_message += '</br>'+prop+'</br>'+r.response.data[prop]
              }}

            } else {
              error_message = r.response.statusText+' ['+r.response.status+']'
            }
            Swal.fire("Error", "New case could not be added to the database.</br> "+error_message, "error").then(result => {
              if( 401 == r.response.status ){
                window.location.href = '/'
              }
            })

        });
      },
      checkpointSave(){
        if (!this.$route.params.readOnly) {
          console.log('AUTOSAVE')
          this.$http
          .create({headers: { 'Content-Type': 'application/json'}})
          .put(this.url__case_update, this.currentCase )
          .then(response => {
                this.refreshCurrentCase()
                // this.$router.push('/case/edit/'+)
            })
          .catch(function(r) {
            if(r.response && r.response.data){
              var error_message = ''
              if ( typeof(r.response.data) === 'string' ){
                r.response.data.split('{')[1].split('}')[0].split(':').forEach(element => {
                  error_message += element + '</br>'
                });
              } else if(typeof(r.response.data) === 'object'){
                for (var prop in r.response.data) {
                // error_message += '</br>'+prop+': '+r.response.data[prop][0]
                error_message += '</br>'+prop+'</br>'+ r.response.data[prop]
              }}

            } else {
              error_message = r.response
            }
            Swal.fire("Error", "Checkpoint save couldn't complete successfully.</br> "+error_message, "error")           
        })
        }
      },
      validations() {
        var verification_counter = 0
        var number_of_verifications = 0
        var html_string = '<div style="text-align: left !important; font-size: 20px">'
        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="1">'
        html_string += `<label>Instructing Party Name: <b>${this.currentCase.instructing_party.name}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1


        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>IP Reference: <b>${this.currentCase.instructing_party.instruction_party_reference}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="3">'
        html_string += `<label>Medco ID: <b>${this.currentCase.instructing_party.medco_id}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="4">'
        html_string += `<label>Instruction Received at: <b>${moment(this.currentCase.instructing_party.instruction_received_at).format("DD/MM/YYYY HH:mm")}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Claimant Title: <b>${this.currentCase.claimant.title}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Claimant First Name: <b>${this.currentCase.claimant.first_name}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Claimant Last Name: <b>${this.currentCase.claimant.last_name}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Claimant DOB: <b>${moment(this.currentCase.claimant.date_of_birth).format("DD/MM/YYYY")}</b></li>`
        html_string += '</input></div>'
        number_of_verifications += 1


        for (var address in this.currentCase.claimant.addresses){
          if (this.currentCase.claimant.addresses[address].primary){
            html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
            html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
            html_string += `<label>Claimant Primary Address: <b>${this.currentCase.claimant.addresses[address].address1}</b>, <b>${this.currentCase.claimant.addresses[address].address2}</b>, <b>${this.currentCase.claimant.addresses[address].address3}</b>, <b>${this.currentCase.claimant.addresses[address].postcode}</b></label>`
            html_string += '</input></div>'
            number_of_verifications += 1

            html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
            html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="3">'
            html_string += `<label>Claimant Phone Number: <b>${this.currentCase.claimant.addresses[address].mobile1}</b></label>`
            html_string += '</input></div>'
            number_of_verifications += 1
            break
          }
        }

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Date Of Accident: <b>${moment(this.currentCase.accident.date).format("DD/MM/YYYY")}</b></label>`
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<div class="md-layout-item md-size-100" style="text-align: left">'
        html_string += '<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="verification_checkboxes" value="2">'
        html_string += `<label>Records Review: <b>${this.currentCase.instructing_party.records_required}</b></label>`
        html_string += '</div>'
        html_string += '</input></div>'
        number_of_verifications += 1

        html_string += '<style>'
        html_string += 'input[type="checkbox"]{'
        html_string += '    -webkit-appearance: initial;'
        html_string += '    appearance: initial;'
        html_string += '    background: gray;'
        html_string += '    width: 20px;'
        html_string += '    height: 20px;'
        html_string += '    border: none;'
        html_string += '    position: relative;'
        html_string += '}'
        html_string += 'input[type="checkbox"]:checked {'
        html_string += '    background: green;'
        html_string += '}'
        html_string += 'input[type="checkbox"]:checked:after {'
        html_string += '    /* Heres your symbol replacement */'
        html_string += '    content: "✓";'
        html_string += '    color: #fff;'
        html_string += '    /* The following positions my tick in the center, '
        html_string += '     * but you could just overlay the entire box'
        html_string += '     * with a full after element with a background if you want to */'
        html_string += '    position: absolute;'
        html_string += '    left: 50%;'
        html_string += '    top: 50%;'
        html_string += '    -webkit-transform: translate(-50%,-50%);'
        html_string += '    -moz-transform: translate(-50%,-50%);'
        html_string += '    -ms-transform: translate(-50%,-50%);'
        html_string += '    transform: translate(-50%,-50%);'
        html_string += '    /*'
        html_string += '     * If you want to fully change the check appearance, use the following:'
        html_string += '     * content: " ";'
        html_string += '     * width: 100%;'
        html_string += '     * height: 100%;'
        html_string += '     * background: blue;'
        html_string += '     * top: 0;'
        html_string += '     * left: 0;'
        html_string += '     */'
        html_string += '}'
        html_string += '</style>'

        Swal.fire({
          title: 'Make sure you verify this!',
          html: html_string,
          type: 'warning',
          width: '1000px',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Verified!',
          cancelButtonText: "Exit",
          preConfirm: () => {
            document.getElementsByName('verification_checkboxes').forEach(element => {
            if (element.checked){
                verification_counter += 1
            }
            });
          }
        }).then((result) => {
          if (result.value) {
            if (verification_counter < number_of_verifications){
              Swal.fire(
                      'Oops...',
                      'Please tick all checkboxes to save the case',
                      'error'
              )
              return;
            }
            if (this.currentCase.draft){
              Swal.fire({
                  title: 'This is a new case!',
                  text: "Do you want to email the file handler?",
                  type: 'warning',
                  showCancelButton: true,
                  confirmButtonColor: '#3085d6',
                  cancelButtonColor: '#d33',
                  confirmButtonText: 'Yes, send email!',
                  cancelButtonText: "No, don't email!"
                }).then((result) => {
                  if (result.value) {
                    this.saveCase(true)
                  }else if(result.dismiss === 'cancel'){
                    this.saveCase(false)
                  }
                })
            }else{
              this.saveCase(false)
            }
          }
        })
      },
      wizardComplete() {
        console.log('wizardComplete')
        console.log(this.$route.name)
        this.validations();
      },
      saveCase(email_filehandler){
          if (this.$route.name === 'EditCase'){
            this.currentCase.wizardComplete = true
            this.currentCase.email_filehandler = email_filehandler
            this.$http
              .create({headers: { 'Content-Type': 'application/json'}})
              .put(this.url__case_update, this.currentCase )
              .then(response => {
                    Swal.fire("Good job!", "The case successfully modified", "success")
                    this.refreshCurrentCase()
                    this.$router.push('/case')
                })
              .catch(function(r) {
                if(r.response && r.response.data){
                  var error_message = ''
                  if ( typeof(r.response.data) === 'string' ){
                    r.response.data.split('{')[1].split('}')[0].split(':').forEach(element => {
                      error_message += element + '</br>'
                    });
                  } else if(typeof(r.response.data) === 'object'){
                    for (var prop in r.response.data) {
                    // error_message += '</br>'+prop+': '+r.response.data[prop][0]
                    error_message += '</br>'+prop+'</br>'+ r.response.data[prop]
                  }}

                } else {
                  error_message = r.response
                }
                Swal.fire("Error", "The case could not be updated.</br> "+error_message, "error")           
            })
          } else if (this.$route.name === 'AddCase') {
            this.$http
              .create({headers: { 'Content-Type': 'application/json'}})
              .post(this.url__case_create, this.currentCase )
              .then(response => {
                    console.log(response)
                    this.$http
                      .get(this.url__case_details+response.data.id+'/' )
                      .then(response => {
                        console.log(response.data)
                        Swal.fire("Good job!", "New case added to the database", "success")
                        this.setCurrentCase(response.data)
                        this.refreshCurrentCase()
                        this.$router.push('/case/edit/'+response.data.id+'/')
                      })
                      .catch(function(error) {
                        console.error(error.response)
                        throw error
                      });
                })
              .catch(function(r) {
                if(r.response && r.response.data){
                  var error_message = ''
                  if ( typeof(r.response.data) === 'string' ){
                    r.response.data.split('\n').splice(0,2)
                    r.response.data.split('\n').splice(0,2).forEach(element => {
                      error_message += element+'</>'
                    });
                  } else if(typeof(r.response.data) === 'object'){
                    for (var prop in r.response.data) {
                    // error_message += '</br>'+prop+': '+r.response.data[prop][0]
                    error_message += '</br>'+prop+'</br>'+r.response.data[prop]
                  }}

                } else {
                  error_message = r.response.statusText+' ['+r.response.status+']'
                }
                Swal.fire("Error", "New case could not be added to the database.</br> "+error_message, "error").then(result => {
                  if( 401 == r.response.status ){
                    window.location.href = '/'
                  }
                })

            });
          }else{
            Swal.fire(
              'WOW!',
              'Please contact the developer. You found a bug he is looking for!',
              'error'
            )
            return
          }
      },
      navigateToTab(tabDef){
        var tabIndex = -1        
        if(tabDef){  
          if(typeof(tabDef) == "string"){
            try{
              tabIndex = parseInt(tabDef)
              if(!tabIndex || tabIndex < 0){
                this.$refs['simple-wizard'].tabs.forEach((t, idx) => {
                  if(tabDef == t.$options.propsData.label){
                    tabIndex = idx
                  }
                })  
              }
            }catch(e){
              console.log("The tab definition passed as a label. It needs translation, but the generic one is insufficient. Error:", e)
            }
          } else if(typeof(tabDef) == "number"){
            tabIndex = tabDef
          }
        }
        if(tabIndex && tabIndex >= 0){
          console.log("Navigating to tab: ",tabDef,' => ',tabIndex)
          this.$refs['simple-wizard'].activeTabIndex = tabIndex
        }

      },
      tabChange(oldTab, newTab){
        setTimeout(function (){window.scroll(0, 0)}, 1)
        this.updateFocus(oldTab, newTab)  
      },
      updateFocus(oldTab, newTab) {
        if (newTab.label === "claimant") {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.ClaimantAttachmentTypes
          this.focus = this.ClaimantAttachmentTypes
        }
        else if (newTab.label === "appointments") {
          this.should_display_attachments_component = false
          this.should_display_requests_component = true
          this.AttachmentTypes = this.AppointmentsAttachmentTypes
          this.focus = this.AppointmentsAttachmentTypes
        }
        else if (newTab.label === "changelog") {
          this.should_display_attachments_component = false
          this.should_display_requests_component = false
          this.AttachmentTypes = this.ChangelogAttachmentTypes
          this.focus = this.ChangelogAttachmentTypes
        }
        else if (newTab.label === "attachments") {
          this.should_display_attachments_component = false
          this.should_display_requests_component = false
          this.AttachmentTypes = this.AttachmentsAttachmentTypes
          this.focus = this.AttachmentsAttachmentTypes
        }
        else if (newTab.label ==="records") {
          this.should_display_attachments_component = false
          this.should_display_requests_component = false
          this.AttachmentTypes = this.RecordsAttachmentTypes
          this.focus = this.RecordsAttachmentTypes
        }
        else if (newTab.label ==="accounts") {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.AccountsAttachmentTypes
          this.focus = this.AccountsAttachmentTypes
        }
        else if (newTab.label === "instructing_party") {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.InstructingPartyAttachmentTypes
          this.focus = this.InstructingPartyAttachmentTypes
        }
        else if (newTab.label === "accident") {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.AccidentAttachmentTypes
          this.focus = this.AccidentAttachmentTypes
        }
        else if (newTab.label ==='instructions') {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.InstructionsAttachmentTypes
          this.focus = this.InstructionsAttachmentTypes
        }
        else if (newTab.label === "insurance"){
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.AttachmentTypes = this.InsuranceAttachmentTypes
          this.focus = this.InsuranceAttachmentTypes
        }
        else if (newTab.label ==="records") {
          this.caseAttachmentVisibility = false
          this.should_display_requests_component = false
          this.focus = ["record"]
        }
        else {
          this.should_display_attachments_component = true
          this.should_display_requests_component = false
          this.focus = [] // display all types
        }
      },
    },
    created() {
      window.addEventListener('resize', this.handleResize)
      this.handleResize();
      if (this.$route.params.id && !this.$route.params.case){
        console.log('GETTING THE CASE AGAIN!!!')
        NProgress.start()
        this.$http
          .get(this.url__case_details+this.$route.params.id+'/')
          .then(response => {
            this.setCurrentCase(response.data)
            this.setCurrentCaseLabel(response.data.label)
            NProgress.done()
          })
          .catch(function(error) {
            console.error(error.response);
            NProgress.done()
            Swal.fire(
              'Oops..',
              'Case details could not be retrieved from the Database',
              'error'
            )
          });
      }else if (!this.$route.params.id){
        console.log('createDummyCase!!!')
        this.createDummyCase()
      }
    },
    beforeDestroy() {
      window.removeEventListener('resize', this.handleResize)
    },
    mounted() {
      console.log('mounted:', this.$route.params.id)
      if (this.$route.params.id){
          this.tabs_checked_by_default = ['tab_appointments', 'tab_changelog', 'tab_attachments', 'tab_medical_reports',
            'tab_accounts', 'tab_complaints', 'tab_data_security', 'tab_instructing_party', 'tab_claimant', 'tab_accident', 
            'tab_instructions' ,'tab_insurance', 'tab_records']
      }
      for (let index = 0; index < this.tabs_checked_by_default.length; index++) {
        const tab_ref = this.tabs_checked_by_default[index];
        if(this.$refs[tab_ref]){
          this.$refs[tab_ref].checked = true
        }
      }
      if(this.$route.params.tab){
        this.navigateToTab(this.$route.params.tab)
      }
    },
    computed: {
      ...mapGetters([
          'currentCase',
          'currentCaseLabel',
      ])
    }
  }
</script>

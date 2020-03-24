<template>
  <div>
    <div class="md-layout-item">
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-green">
          <div class="card-icon">
            <md-icon>folder_shared</md-icon>
          </div>
          <h4 class="title">Cases</h4>

        <md-card-actions>
          <div v-if="currentCase && currentCase.id && currentCase.status === 'Cancelled'">
            <md-button class="md-icon-button md-just-icon md-success" title="Open Selected Case" v-on:click="openCurrentCase()">
              <i class="far fa-folder-open"></i>
            </md-button>
          </div>
          <div v-else-if="currentCase && currentCase.id && currentCase.status === 'On Hold'">
            <md-button class="md-icon-button md-just-icon md-danger" title="Cancel Selected Case" v-on:click="cancelCurrentCase()">
              <i class="fas fa-power-off"></i>
            </md-button>
            <md-button class="md-icon-button md-just-icon md-success" title="Open Selected Case" v-on:click="openCurrentCase()">
              <i class="far fa-folder-open"></i>
            </md-button>
          </div>
          <div v-else-if="currentCase && currentCase.id">
            <md-button class="md-icon-button md-just-icon md-danger" title="Cancel Selected Case" v-on:click="cancelCurrentCase()">
              <i class="fas fa-power-off"></i>
            </md-button>
            <md-button class="md-icon-button md-just-icon md-danger" title="Put Selected Case On Hold" v-on:click="onHoldCurrentCase()">
              <i class="far fa-pause-circle"></i>
            </md-button>
          </div>
          <router-link  v-if="currentCase && currentCase.id" :to="{ name: 'EditCase', params: { id: currentCase.id, case: currentCase, readOnly: true }}">
            <md-button class="md-icon-button md-just-icon md-primary">
              <md-icon>visibility</md-icon>
              <md-tooltip><b>Read-only</b> mode</md-tooltip>
            </md-button>
          </router-link>
          <router-link  v-if="!currentCase.id" :to="{ name: 'AddCase', params: { id: null, case: getMainObjectTemplate(null) }}">
            <md-button class="md-icon-button md-just-icon md-info">
              <md-icon>add</md-icon>
              <md-tooltip><b>Add</b> NEW Case</md-tooltip>
            </md-button>
          </router-link>
          <router-link  v-if="currentCase && currentCase.id" :to="{ name: 'EditCase', params: { id: currentCase.id, case: currentCase }}">
            <md-button class="md-icon-button md-just-icon md-warning">
              <md-icon>edit</md-icon>
              <md-tooltip><b>Edit</b> mode</md-tooltip>
            </md-button>
          </router-link>
          <!-- <md-button  v-if="currentCase && currentCase.id" class="md-icon-button md-just-icon md-danger" @click.native="handleDelete(currentCase)">
            <md-icon>delete</md-icon>
          </md-button> -->
        </md-card-actions>

        </md-card-header>
        <md-card-content>
          <div class="md-layout" style="text-align: center">
            <div class="md-layout-item inputBox">
              <md-field>
                <label>Search by:</label>
                <md-select
                  v-model="search_criteria">
                  <md-option value="ip_reference">Instructing Party Reference</md-option>
                  <md-option value="ip_name">Instructing Party Name</md-option>
                  <md-option value="our_ref">Our Reference</md-option>
                  <md-option value="full_name">Full Name</md-option>
                  <md-option value="first_name">First Name</md-option>
                  <md-option value="last_name">Last Name</md-option>
                  <md-option value="medco_id">MedCo ID</md-option>
                  <md-option value="invoice_number">Invoice #</md-option>
                </md-select>
              </md-field>
            </div>
            <div class="md-layout-item md-size-25 inputBox">
              <md-field>
                <label>Search for:</label>
                <md-input
                  autocomplete="__none__"
                  v-model="search_input"
                  type="text"></md-input>
              </md-field>
            </div>
            <div class="md-layout-item md-size-25 inputBox">
              <md-checkbox v-model="search_everywhere"><span style="font-size: 20px"><b>Match anywhere in {{this.search_everywhere_string}}</b></span></md-checkbox>
            </div>
            <div class="md-layout-item md-size-25 inputBox">
              <md-button style="width: 100%" class="md-primary" v-on:click="searchDatabase()"><i class="fas fa-search"></i>Search</md-button>
            </div>
          </div>
          <md-table v-if="queriedData.length" :key="componentKey" :value="queriedData" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" class="paginated-table table-striped table-hover inputBox" md-fixed-header  @md-selected="onSelect" table-header-color="green">
            <md-table-toolbar>
              <md-field>
                <label for="pages">Per page</label>
                <md-select v-model="pagination.perPage" name="pages">
                  <md-option
                    v-for="item in pagination.perPageOptions"
                    :key="item"
                    :label="item"
                    :value="item">
                    {{ item }}
                  </md-option>
                </md-select>
              </md-field>

              <md-field>
                <md-input
                  type="search"
                  class="mb-3"
                  clearable
                  style="width: 200px"
                  placeholder="Search records"
                  v-model="searchQuery">
                </md-input>
              </md-field>
            </md-table-toolbar>

            <md-table-row slot="md-table-row" slot-scope="{ item }" md-selectable="single" md-auto-select>
              <md-table-cell md-label="Our Reference" md-sort-by="reference">{{ item.reference }}</md-table-cell>
              <md-table-cell md-label="Claimant" md-sort-by="claimant">{{ item.claimant }}</md-table-cell>
              <md-table-cell md-label="MedCo" md-sort-by="medco">{{ item.medco }}</md-table-cell>
              <md-table-cell v-if="window.width > max_screen_width - 100" md-label="DOB" md-sort-by="date_of_birth">{{ item.date_of_birth | changeDateFilter }}</md-table-cell>
              <md-table-cell md-label="IP Reference" md-sort-by="ip_reference">{{ item.ip_reference | ipRefFilter }}</md-table-cell>
              <md-table-cell v-if="window.width > max_screen_width - 150" md-label="IP" md-sort-by="ip">{{ item.ip }}</md-table-cell>
              <!-- <md-table-cell md-label="IP File Handler" md-sort-by="ip_file_handler">{{ item.ip_file_handler }}</md-table-cell> -->
              <md-table-cell v-if="window.width > max_screen_width - 250" md-label="Claimant Postcode" md-sort-by="postcode">{{ item.postcode }}</md-table-cell>
              <md-table-cell v-if="window.width > max_screen_width - 350" md-label="Claimant Address" md-sort-by="address">{{ item.address }}</md-table-cell>
              <md-table-cell v-if="window.width > max_screen_width - 450" md-label="DOA" md-sort-by="accident_date">{{ item.accident_date | changeDateFilter }}</md-table-cell>
              <!-- <md-table-cell md-label="Report Date" md-sort-by="report_date">{{ item.report_date }}</md-table-cell>
              <md-table-cell md-label="Date Instruction Received" md-sort-by="date_instruction_received">{{ item.date_instruction_received }}</md-table-cell> -->
              <!-- <md-table-cell md-label="Invoice No" md-sort-by="invoice_no">{{ item.invoice_no }}</md-table-cell> -->
            </md-table-row>
          </md-table>
        </md-card-content>
        <md-card-actions md-alignment="space-between">
          <div class="">
            <p class="card-category">Showing {{from + 1}} to {{to}} of {{total}} entries</p>
          </div>
          <pagination class="pagination-no-border pagination-success"
                        v-model="pagination.currentPage"
                        :per-page="pagination.perPage"
                        :total="total">
          </pagination>
        </md-card-actions>
      </md-card>
    </div>
  </div>

</template>

<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
import { Pagination } from "vue-material-dashboard-pro/src/components";
import moment from 'moment';
import Fuse from "fuse.js"
import Swal from "sweetalert2"

import CaseForm from "./CaseForm.vue";

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
    ipRefFilter:
    function (value) {
      if (value){
        return value.replace('/', '/ ')
      }
    }
  },
  components: {
    Pagination,
    CaseForm
  },
  computed: {
    ...mapGetters([
        'currentCase',
        'currentCaseLabel',
    ]),
    /***
     * Returns a page from the searched data or the whole data. Search is performed in the watch section below
     */
    queriedData() {
      let result = this.tableData;
      if (this.searchedData.length > 0) {
        result = this.searchedData;
      }
      return result.slice(this.from, this.to);
    },
    to() {
      let highBound = this.from + this.pagination.perPage;
      if (this.total < highBound) {
        highBound = this.total;
      }
      return highBound;
    },
    from() {
      return this.pagination.perPage * (this.pagination.currentPage - 1);
    },
    total() {
      return this.searchedData.length > 0
        ? this.searchedData.length
        : this.tableData.length;
    },

  },
  data() {
    return {
      search_everywhere: false,
      search_everywhere_string: '',
      search_criteria: null,
      search_input: null,
      max_screen_width: 0,
      componentKey: 0,
      window: {
        width: 0,
        height: 0
      },
      currentSort: "name",
      currentSortOrder: "asc",
      pagination: {
        perPage: 5,
        currentPage: 1,
        perPageOptions: [5, 10, 25, 50, 100, 1000],
        total: 0
      },
      searchQuery: "",
      propsToSearch: [
        "reference",
        "claimant",
        "medco",
        "date_of_birth",
        "ip_reference",
        "ip",
        "ip_file_handler",
        "postcode",
        "address",
        "accident_date",
        "date_instruction_received",
        "invoice_no"
      ],
      tableData: [],
      searchedData: [],
      fuseSearch: null,
      searchBy: [
        "Reference",
        "Claimant",
        "MedCo",
        "Date Of Birth",
        "IP Reference",
        "IP",
        "IP File Handler",
        "Postcode",
        "Address",
        "Date of accident",
        "Date Instruction Received",
        "Invoice No"
      ],
      selected: {},
      edited: null,
      formOptions: {},
      showDialog: false
    };
  },
  methods: {
    ...mapActions([
      'setCurrentCase',
      'setCurrentCaseLabel',
      'refreshCurrentCase'
    ]),
    searchDatabase(){
      if (this.search_input || this.search_criteria === 'all_medco_cases' || this.search_criteria === 'all_cases' || this.search_criteria === 'awaiting_report' || this.search_criteria === 'awaiting_instruction'){
        if (this.search_input){
          this.search_input = this.search_input.trim()
        }
        NProgress.start()
        this.$http
          .post(this.url__case_filtered_quick_search_compact, {'search_criteria': this.search_criteria, 'search_input': this.search_input, 'search_everywhere': this.search_everywhere })
          .then(response => {
            if (response.data.length){
              this.tableData = response.data;
              // Fuse search initialization.
              this.fuseSearch = new Fuse(this.tableData, {
                keys: [
                  "reference",
                  "claimant",
                  "medco",
                  "date_of_birth",
                  "ip_reference",
                  "ip",
                  "ip_file_handler",
                  "postcode",
                  "address",
                  "accident_date",
                  "date_instruction_received",
                  "invoice_no"
                  ],
                  threshold: 0.2
                });
              NProgress.done()
            }else{
              this.tableData = []
              console.log('NO DATA!!!')
              NProgress.done()
              Swal.fire({
                position: 'center-center',
                type: 'warning',
                title: 'No matching results found in the database!',
                showConfirmButton: false,
              })
            }
          })
          .catch(function(error) {
            console.error(error.response)
            NProgress.done()
          });
        }else{
          Swal.fire({
            position: 'center-center',
            type: 'warning',
            title: 'Please enter search Criteria',
            showConfirmButton: false,
            timer: 1000
          })
          // Swal.fire(
          //   'Please enter search Criteria'
          // )
        }
    },
    openCurrentCase(){
      var item = JSON.parse(sessionStorage.getItem('current_case_object'))
      var reference = "-" + item.id;
      if (item.claimant.last_name){
        reference = item.claimant.last_name.substring(0,3) + item.id;
      }
      Swal.fire({
          type: 'warning',
          title: 'Are you sure?',
          html: 'Do you want to open the case: <b>' + reference + '</b> ?',
          showCancelButton: true,

        }).then(result => {
          if (result.value) {
            this.$http
              .post(this.url__case_open, {'case_id': item.id})
              .then(response => {
                Swal.fire({
                  width: '1000px',
                  type: 'success',
                  title: 'Case Opened',
                  html: 'Selected Case has been opened',
                })
                this.refreshCurrentCase()                  
              })
              .catch(function(error) {
                  console.error(error.response);
              })
          }
        })
    },
    cancelCurrentCase() {
      var item = JSON.parse(sessionStorage.getItem('current_case_object'))
      var send_email = false
      var dynamic_html = ''
      var now_datetime = moment(new Date())
      for (var index in item.appointments){
        if (moment(item.appointments[index].slot.datetime) >= now_datetime){
          if (!item.appointments[index].cancelled && !item.appointments[index].attended && !item.appointments[index].dna){
            dynamic_html += '<span style="font-size: 25px"><br><b>' + moment(item.appointments[index].slot.datetime).format('DD/MM/YYYY HH:mm') + ' with ' + item.appointments[index].slot.expert + '</b></br></span>'
          }
        }
      }
      if (dynamic_html){
        dynamic_html = '<u>The following Appointments will be cancelled:</u>' + dynamic_html
      }
      var our_ref = ''
      if (item.claimant.last_name){
        our_ref = item.claimant.last_name.substring(0,3) + item.id
      }else{
        our_ref = `-${item.id}`
      }
      Swal.fire({
        width: '1000px',
        type: 'warning',
        title: 'Are you sure you want to cancel the case: ' + our_ref,
        html: dynamic_html
              +'<div class="md-layout-item md-size-100" style="text-align:center">'
              +'<input type="checkbox" style="transform: scale(2);display:inline-block;vertical-align:middle;" class="md-checkbox" id="email_expert" value=true checked>'
              +'<label style="font-size: 25px">Email Experts that Claimant has upcoming appointments with?</label>'
              +'</input>'
              +'</div>',
        showCancelButton: true,
        preConfirm: () => {
          if (document.getElementById('email_expert').checked){
            send_email = true
          }
        }
      }).then(result => {
        if (result.value) {
          this.$http
            .post(this.url__case_cancel, {'case_id': item.id, 'send_email': send_email})
            .then(response => {
              if (response.data.status){
                Swal.fire({
                  width: '1000px',
                  type: 'success',
                  title: 'Cancellation status',
                  html: response.data.status,
                })
              }
              this.refreshCurrentCase()                         
            })
            .catch(function(error) {
                console.error(error.response);
            })
        }
      })

    },
    onHoldCurrentCase(){
      var item = JSON.parse(sessionStorage.getItem('current_case_object'))
      var reference = "-" + item.id;
      if (item.claimant.last_name){
        reference = item.claimant.last_name.substring(0,3) + item.id;
      }
      var send_email = false
      var dynamic_html = ''
      var now_datetime = new Date()
      for (var index in item.appointments){
        if (moment(item.appointments[index].slot.datetime) >= now_datetime){
          if (!item.appointments[index].cancelled && !item.appointments[index].attended && !item.appointments[index].dna){
            dynamic_html += '<span style="font-size: 25px"><br><b>' + moment(item.appointments[index].slot.datetime).format('DD/MM/YYYY HH:mm') + ' with ' + item.appointments[index].slot.expert + '</b></br></span>'
          }
        }
      }
      if (dynamic_html){
        dynamic_html = '<u>The following Appointments will be cancelled:</u>' + dynamic_html
      }
      Swal.fire({
        width: '1000px',
        type: 'warning',
        title: 'Are you sure you want to put on hold the case: ' + reference,
        html: dynamic_html
              +'<div class="md-layout-item md-size-100" style="text-align:center">'
              +'<input type="checkbox" style="transform: scale(2);display:inline-block;vertical-align:middle;" class="md-checkbox" id="email_expert" value=true checked>'
              +'<label style="font-size: 25px">Email Experts that Claimant has upcoming appointments with?</label>'
              +'</input>'
              +'</div>',
        showCancelButton: true,
        preConfirm: () => {
          if (document.getElementById('email_expert').checked){
            send_email = true
          }
        }
      }).then(result => {
        if (result.value) {
          this.$http
            .post(this.url__case_on_hold, {'case_id': item.id, 'send_email': send_email})
            .then(response => {
              if (response.data.status){
                Swal.fire({
                  width: '1000px',
                  type: 'success',
                  title: 'Case On Hold status',
                  html: response.data.status,
                })
              }
              this.refreshCurrentCase()                         
            })
            .catch(function(error) {
                console.error(error.response);
            })
        }
      })
    },
    handleResize() {
      this.window.width = window.innerWidth;
      this.window.height = window.innerHeight;
      this.componentKey += 1
    },
    customSort(value) {
      return value.sort((a, b) => {
        const sortBy = this.currentSort;
        if (this.currentSortOrder === "desc") {
          return a[sortBy].localeCompare(b[sortBy]);
        }
        return b[sortBy].localeCompare(a[sortBy]);
      });
    },
    handleAdd() {
      Swal.fire({
        title: `Adding new case`,
        buttonsStyling: false,
        type: "success",
        confirmButtonClass: "md-button md-success"
      });
    },
    handleEdit(item) {
      Swal.fire({
        title: `You want to edit ${item.building_name}`,
        buttonsStyling: false,
        confirmButtonClass: "md-button md-info"
      });
    },
    handleDelete(item) {
      Swal.fire({
        title: "Are you sure?",
        text: `You won"t be able to revert this!`,
        type: "warning",
        showCancelButton: true,
        confirmButtonClass: "md-button md-success btn-fill",
        cancelButtonClass: "md-button md-danger btn-fill",
        confirmButtonText: "Yes, delete it!",
        buttonsStyling: false
      }).then(result => {
        if (result.value) {
          this.deleteRow(item, this.tableData);
        }
      });
    },
    deleteRow(item, table) {
      this.$http
        .delete(this.url__case + item.id)
        .then(response => {
          Swal.fire({
            title: "Deleted!",
            text: `You deleted ${item.name}`,
            type: "success",
            confirmButtonClass: "md-button md-success btn-fill",
            buttonsStyling: false
          });
        })
        .then(function() {
          console.log(item);
          let indexToDelete = table.findIndex(
            tableRow => tableRow.id === item.id
          );
          console.log(indexToDelete);
          if (indexToDelete >= 0) {
            table.splice(indexToDelete, 1);
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    onSelect(item) {
      NProgress.start()
      this.selected = item;
      console.log(item)

      if (item){
        this.$http
        .get(this.url__case_details+item.id+'/' )
        .then(response => {
          this.setCurrentCase(response.data)
          this.setCurrentCaseLabel(response.data.label)
          NProgress.done()
        })
        .catch(function(error) {
          console.error(error.response);
          NProgress.done()
          Swal.fire(
            'Oops...',
            'Could not get the case details from the database!',
            'error'
          )
        }); 
      }else{
        NProgress.done()
        Swal.fire(
            'Oops...',
            'Case not selected properly. Please reload and select again!',
            'error'
          )
      }
    },
    keyPressed(k){
      if (k.code == 'Enter'){
        console.log('ENTER WAS PRESSED')
        this.searchDatabase()
      }
    },
    getMainObjectTemplate(selected) {
      console.log(" >> getEmptyCaseObject <<" )
      var emptyObject = {
          label: null,
          selection_date: null,
          date_created: null,
          instructing_party: {
            instruction_received_at: null,
            name: null,
            medco_id: null,
            po_number: null,
            instruction_party_reference: null,
            type: null,
            records_required: null,
            file_handler: null,
            file_handlers: [],
            products: []
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
            recommended_appointment_date: null,
            venue_parking: null,
            venue_disable_access: null,
            venue_lift_access: null,
            venue_child_friendly: null
          },
          insurance: {
            company: null,
            postcode: null,
            address1: null,
            address2: null,
            address3: null,
            telephone: null,
            facsimile: null,
            third_party_name: null,
            file_handler: null,
            direct_telephone: null,
            email: null
          },
          complaints: [],
          data_security: [],
          appointments: [],
          accounts: {
            invoices: [],
            payments: []
          },
          longlat: null
        }
        if (selected) {
          var derived_object = Object.assign(emptyObject, selected);
          return derived_object;
        }
        return emptyObject;
      }
  },
  mounted() {
    // NProgress.start()
    // this.$http
    //   .get(this.url__case_list_compact,  { params: this.$route.query })
    //   .then(response => {
    //     this.tableData = response.data;
    //     // Fuse search initialization.
    //     this.fuseSearch = new Fuse(this.tableData, {
    //       keys: [
    //         "reference",
    //         "claimant",
    //         "medco",
    //         "date_of_birth",
    //         "ip_reference",
    //         "ip",
    //         "ip_file_handler",
    //         "postcode",
    //         "address",
    //         "accident_date",
    //         "date_instruction_received",
    //         "invoice_no"
    //         ],
    //         threshold: 0.2
    //       });
    //     NProgress.done()
    //   })
    //   .catch(function(error) {
    //     console.error(error.response)
    //     NProgress.done()
    //   });
  },
  created(){
    window.addEventListener('resize', this.handleResize)
    this.max_screen_width = window.screen.availWidth
    // this.handleResize();
    window.addEventListener('keypress', this.keyPressed)
    if (this.$route.params.search_criteria === 'all_medco_cases'){
      this.search_criteria = 'all_medco_cases'
      this.searchDatabase();
    }else if (this.$route.params.search_criteria === 'all_cases'){
      this.search_criteria = 'all_cases'
      this.searchDatabase();
    }else if(this.$route.params.search_criteria === 'awaiting_report'){
      this.search_criteria = 'awaiting_report'
      this.searchDatabase();
    }else if(this.$route.params.search_criteria === 'awaiting_instruction'){
      this.search_criteria = 'awaiting_instruction'
      this.searchDatabase();
    }
  },
  beforeDestroy: function () {
    // remove listener
    window.removeEventListener('keypress', this.keyPressed)
    window.removeEventListener('resize', this.handleResize)
  },
  watch: {
    /**
     * Searches through the table data by a given query.
     * NOTE: If you have a lot of data, it"s recommended to do the search on the Server Side and only display the results here.
     * @param value of the query
     */
    searchQuery(value) {
      let result = this.tableData;
      if (value !== "") {
        result = this.fuseSearch.search(this.searchQuery);
      }
      this.searchedData = result;
    },
    search_criteria(value) {
      console.log(value)
      if (value == 'medco_id'){
        this.search_everywhere_string = 'MedCo ID'
      }else if(value == 'ip_reference'){
        this.search_everywhere_string = 'IP Reference'
      }else if(value == 'our_ref'){
        this.search_everywhere_string = 'Our ref'
      }else if(value == 'full_name'){
        this.search_everywhere_string = 'Full Name'
      }else if(value == 'first_name'){
        this.search_everywhere_string = 'First Name'
      }else if(value == 'last_name'){
        this.search_everywhere_string = 'Last Name'
      }else if(value == 'invoice_number'){
        this.search_everywhere_string = 'Invoice #'
      }else if(value == 'ip_name'){
        this.search_everywhere_string = 'IP Name'
      }
    }
  }
};
</script>

<style>
.md-table .md-table-cell.md-has-action .md-table-cell-container {
  text-align: center;
  justify-content: center;
}
.md-table-head {
  text-align: center;
  border-bottom: 1px solid;
}
.md-table .md-table-cell {
  text-align: center;
  border: 1px solid;
}
</style>
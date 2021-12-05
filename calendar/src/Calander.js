import React from 'react';
import { useState } from 'react';
import Tooltip from '@material-ui/core/Tooltip';
import { DataTypeProvider } from '@devexpress/dx-react-grid';
import { Grid, Table, TableHeaderRow } from '@devexpress/dx-react-grid-material-ui';

const columns = [
  { name: 'name', title: 'Name' },
  { name: 'acronym', title: 'Acronym' },
  { name: 'submission', title: 'Submission' },
  { name: 'notification', title: 'Notification' },
  { name: 'conference', title: 'Conference' },
  { name: 'location', title: 'Location' },
];

const rows = [
  { name: '7th International Conference on Signal Processing and Integrated Networks', acronym: '', submission: '11/11/2019', notification: '12/9/2019', conference: '2/27/2020 - 3/1/2020', location: 'Delhi/NCR, India' },
  { name: '7th International Conference on Signal Processing and Integrated Networks', acronym: 'SPIN 2020', submission: '11/11/2019', notification: '12/9/2019', conference: '2/27/2020', location: 'Noida- Delhi NCR, India' },
];

const titleStyle = {
  color: "black", 
  backgroundColor: "powderblue",
  textAlign: "center",
  fontSize: "200%",
  fontFamily: "verdana",
  border: "5px solid powderblue"
}

const TooltipFormatter = ({ row: { name }, value }) => (
  <Tooltip title={(
    <span>
      {name}
    </span>
  )}
  >
    <span>
      {value}
    </span>
  </Tooltip>
);

const CellToolTip = props => (
  <DataTypeProvider
    for={columns.map(({ name }) => name)}
    formatterComponent={TooltipFormatter}
    {...props}
  />
);

function Calander() {
  const [tableColumnExtensions] = useState([
    { columnName: 'name', width: '300' , wordWrapEnabled: true},
    { columnName: 'acronym', width: 'auto' , wordWrapEnabled: true },
    { columnName: 'submission', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'notification', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'conference', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'location', width: 'auto' , wordWrapEnabled: true},
  ]);

    return (
      <div class="calander">
        <h1 style={titleStyle}>
          NLP Conferences Calendar
          </h1>
        <Grid
          rows={rows}
          columns={columns}
        >
          <CellToolTip />
          <Table columnExtensions={tableColumnExtensions} />
          <TableHeaderRow />
        </Grid>
      </div>
    );
}

export default Calander;
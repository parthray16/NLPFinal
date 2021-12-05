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

const headerStyle = {
    color: "black", 
    backgroundColor: "IndianRed",
    textAlign: "center",
    fontSize: "200%",
    fontFamily: "verdana",
    border: "5px solid IndianRed"
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

function Extraction(props) {
  const [tableColumnExtensions] = useState([
    { columnName: 'name', width: '300' , wordWrapEnabled: true},
    { columnName: 'acronym', width: 'auto' , wordWrapEnabled: true },
    { columnName: 'submission', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'notification', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'conference', width: 'auto' , wordWrapEnabled: true},
    { columnName: 'location', width: 'auto' , wordWrapEnabled: true},
  ]);

    return (
      <div class="extraction">
        <h2 style={headerStyle}>Conferences Extracted</h2>
        <Grid
          rows={props.data}
          columns={columns}
        >
          <CellToolTip />
          <Table columnExtensions={tableColumnExtensions} />
          <TableHeaderRow />
        </Grid>
      </div>
    );
}

export default Extraction;
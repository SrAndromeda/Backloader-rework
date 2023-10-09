import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import {
  Button,
  Checkbox,
  FormControlLabel,
  Grid,
  Icon,
  InputAdornment,
  MenuItem,
  Radio,
  RadioGroup,
  styled,
} from "@mui/material";
import { Span } from "app/components/Typography";
import { useEffect, useState } from "react";
import { TextValidator, ValidatorForm } from "react-material-ui-form-validator";

const TextField = styled(TextValidator)(() => ({
  width: "100%",
  marginBottom: "16px",
}));

const SimpleForm = ({ sendData, outlets=[] }) => {
  const [state, setState] = useState({
    type: 'p', 
    quality: 'a',
  });

  const handleChange = (event) => {
    event.persist();
    setState({ ...state, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    sendData(event, state)
  }

  const handleChangeSelect = (event) => {
    setState({ ...state, [event.target.name]: event.target.value });
  }

  const {
    name,
    url,
    type,
    quality,
    outlet,
    interval
  } = state;

  return (
    <div>
      <ValidatorForm onSubmit={handleSubmit} onError={() => null}>
        <Grid container spacing={6}>
          <Grid item lg={6} md={6} sm={12} xs={12} sx={{ mt: 2 }}>
            <TextField
              type="text"
              name="name"
              label="Flow Name"
              value={name || ""}
              onChange={handleChange}
              errorMessages={["this field is required"]}
              validators={["required", "isString"]}
            />

            <TextField
              type="text"
              name="url"
              label="URL"
              onChange={handleChange}
              value={url || ""}
              validators={["required"]}
              errorMessages={["this field is required"]}
            />

            <TextField
              id="type"
              name="type"
              select
              label="Select type"
              defaultValue="p"
              // validators={["required"]}
              onChange={handleChangeSelect}
            >
              <MenuItem value={'p'}>
                Playlist
              </MenuItem>
              <MenuItem value={'c'}>
                Channel
              </MenuItem>
            </TextField>

            <TextField
              id="quality"
              name="quality"
              select
              label="Select quality"
              defaultValue="a"
              // validators={["required"]}
              onChange={handleChangeSelect}
            >
              <MenuItem value={'a'}>
                Audio
              </MenuItem>
              <MenuItem value={'720'}>
                720p
              </MenuItem>
              <MenuItem value={'1080'}>
                1080p
              </MenuItem>
              <MenuItem value={'1440'}>
                1440p
              </MenuItem>
              <MenuItem value={'2160'}>
                4K
              </MenuItem>
              <MenuItem value={'max'}>
                Best
              </MenuItem>
            </TextField>

            <TextField
              id="outlet"
              name="outlet"
              select
              label="Select outlet"
              defaultValue=""
              // validators={["required"]}
              onChange={handleChangeSelect}
            >
              {outlets
                .map((outlet, index) => {
                  return(
                    <MenuItem value={outlet.id} key={index}>
                      {outlet.name}
                    </MenuItem>
                  )
                })
              }
            </TextField>
            <TextField
              type="number"
              name="interval"
              label="Interval (s)"
              onChange={handleChange}
              value={interval || -1}
              validators={["required", "minNumber:0"]}
              errorMessages={["this field is required", "The interval must be positive"]}
              InputProps={{
                endAdornment: <InputAdornment position="end"><strong>s</strong></InputAdornment>,
              }}
            />
          </Grid>
        </Grid>

        <Button color="primary" variant="contained" type="submit" >
          <Icon>send</Icon>
          <Span sx={{ pl: 1, textTransform: "capitalize" }}>Submit</Span>
        </Button>
      </ValidatorForm>
    </div>
  );
};

export default SimpleForm;

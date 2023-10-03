import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import AdapterDateFns from "@mui/lab/AdapterDateFns";
import {
  Button,
  Checkbox,
  FormControlLabel,
  Grid,
  Icon,
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

const SimpleForm = ({sendData}) => {
  const [state, setState] = useState({
    video: "%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s",
    thumbnail: "%(title)s [%(id)s]/poster.%(ext)s",
    info: "%(title)s [%(id)s]/%(title)s [%(id)s].%(ext)s"
  });

  const handleChange = (event) => {
    event.persist();
    setState({ ...state, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    sendData(event,state)
  }

  const {
    name,
    path,
    video,
    thumbnail,
    info
  } = state;

  return (
    <div>
      <ValidatorForm onSubmit={handleSubmit} onError={() => null}>
        <Grid container spacing={6}>
          <Grid item lg={6} md={6} sm={12} xs={12} sx={{ mt: 2 }}>
            <TextField
              type="text"
              name="name"
              label="Outlet Name"
              value={name || ""}
              onChange={handleChange}
              errorMessages={["this field is required"]}
              validators={["required", "isString"]}
            />

            <TextField
              type="text"
              name="path"
              label="Path"
              onChange={handleChange}
              value={path || ""}
              validators={["required"]}
              errorMessages={["this field is required"]}
            />

            <TextField
              type="text"
              name="video"
              label="Video Storage"
              value={video || ""}
              onChange={handleChange}
              validators={["required"]}
              errorMessages={["this field is required"]}
            />

            <TextField
              type="text"
              name="thumbnail"
              label="Thumbnail Storage"
              value={thumbnail || ""}
              onChange={handleChange}
              validators={["required"]}
              errorMessages={["this field is required"]}
            />

            <TextField
              type="text"
              name="info"
              label="Info Storage"
              value={info || ""}
              onChange={handleChange}
              validators={["required"]}
              errorMessages={["this field is required"]}
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

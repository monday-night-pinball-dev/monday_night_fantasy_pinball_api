 
import { AppShell, Divider,  } from '@mantine/core';
import { FaHome } from 'react-icons/fa';
import { RiTeamFill } from "react-icons/ri";
import { NavLink } from 'react-router-dom';
import classes from '../MnfpAppShell.module.css';
import React, { useState } from 'react';
import { GiPinballFlipper } from "react-icons/gi";
import { PiPersonSimpleThrowBold } from "react-icons/pi";
import { FaTableCellsRowLock } from "react-icons/fa6";  

 

export function MnfpAppShellNavBar() { 
  const [active, setActive] = useState('Billing'); 

  const items = [
    { link: '/home', label: 'Home', icon: <FaHome className={classes.linkIcon} /> },
    { link: '/team', label: 'Team', icon: <RiTeamFill className={classes.linkIcon} /> },
    { link: '/gameday', label: 'Gameday', icon: <GiPinballFlipper className={classes.linkIcon} /> },
    { link: '/players', label: 'Players', icon: <PiPersonSimpleThrowBold className={classes.linkIcon} /> }, 
  ]

  const adminItems = [
    { link: '/admin/users' , label: 'Users', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },
    { link: '/admin/venues' , label: 'Venues', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },
    { link: '/admin/leagueTeams' , label: 'League Teams', icon: <FaTableCellsRowLock className={classes.linkIcon} /> }, 
    { link: '/admin/leaguePlayers' , label: 'League Players', icon: <FaTableCellsRowLock className={classes.linkIcon} /> }, 
    { link: '/admin/fantasyLeagues' , label: 'Fantasy Leagues', icon: <FaTableCellsRowLock className={classes.linkIcon} /> }, 
    { link: '/admin/fantasyTeams' , label: 'Fantasy Teams', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },  
    { link: '/admin/seasons' , label: 'Seasons', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },
    { link: '/admin/fantasyTeamSeasonLinks' , label: 'Fantasy Team Seasons', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },
    { link: '/admin/leaguePlayerFantasyTeamSeasonLinks' , label: 'League Player Fantasy Team Seasons', icon: <FaTableCellsRowLock className={classes.linkIcon} /> },
  ]

  const links = items.map((item) => ( 
    <NavLink
      className={classes.link}
      data-active={active === item.label || undefined}
      to={item.link}
      key={item.label}
      onClick={() => { 
        setActive(item.label);
      }}
    >
      {item.icon}
      <span>{item.label}</span>
    </NavLink>
  ));

  const adminLinks = adminItems.map((item) => ( 
    <NavLink
      className={classes.link}
      data-active={active === item.label || undefined}
      to={item.link}
      key={item.label}
      onClick={() => { 
        setActive(item.label);
      }}
    >
      {item.icon}
      <span>{item.label}</span>
    </NavLink>
  ));

  return (
    <AppShell.Navbar p="md" style={{gap: '10px'}}>
      <AppShell.Section>
        {links}
      </AppShell.Section>
      <Divider label="Admin" labelPosition='center' />
      <AppShell.Section>
        {adminLinks}
      </AppShell.Section>
    </AppShell.Navbar>
  );
}
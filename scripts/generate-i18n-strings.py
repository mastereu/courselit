#!/usr/bin/env python3
"""
Generate locale-aware strings.ts files that read from i18n JSON messages.
This preserves all existing named exports so no component imports need to change.
"""
import re
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apps/web")

def generate_ui_strings():
    """Rewrite ui-config/strings.ts to use i18n messages."""
    src = os.path.join(BASE, "ui-config/strings.ts")
    with open(src, 'r') as f:
        content = f.read()
    
    lines = []
    lines.append('import { Constants } from "@courselit/common-models";')
    lines.append('import { messages } from "../i18n";')
    lines.append('')
    lines.append('const ui = messages.ui;')
    lines.append('')
    lines.append('/**')
    lines.append(' * Application-wide UI strings.')
    lines.append(' * Locale is controlled by NEXT_PUBLIC_LOCALE env var.')
    lines.append(' * Translations are in i18n/messages/<locale>/messages.json')
    lines.append(' */')
    lines.append('')
    
    # Extract all export const lines
    # Handle: export const NAME = "value";
    # Handle: export const NAME = `template`;
    # Handle: export const NAME = Constants.Something;
    # Handle multi-line strings
    
    pattern = re.compile(
        r'^export\s+const\s+(\w+)\s*=\s*(.+?);\s*$',
        re.MULTILINE
    )
    
    # Also handle multi-line exports
    full_pattern = re.compile(
        r'export\s+const\s+(\w+)\s*=\s*((?:[^;]|\n)*?);',
        re.MULTILINE
    )
    
    # Non-translatable constants (empty strings, Constants refs, etc.)
    non_translatable = {
        'GENERIC_LOGO_PATH': '""',
        'GENERIC_CURRENCY_UNIT': '""',
        'GENERIC_STRIPE_PUBLISHABLE_KEY_TEXT': '""',
        'GENERIC_CURRENCY_ISO_CODE': '""',
        'GENERIC_PAYMENT_METHOD': '""',
        'GENERIC_CODE_INJECTION_HEAD': '""',
        'PRICING_FREE': 'Constants.ProductPriceType.FREE',
        'PRICING_EMAIL': 'Constants.ProductPriceType.EMAIL',
        'PRICING_PAID': 'Constants.ProductPriceType.PAID',
    }
    
    seen = set()
    for match in full_pattern.finditer(content):
        name = match.group(1)
        value = match.group(2).strip()
        
        if name in seen:
            continue
        seen.add(name)
        
        if name in non_translatable:
            lines.append(f'export const {name} = {non_translatable[name]};')
        else:
            lines.append(f'export const {name} = ui.{name} ?? {value};')
    
    lines.append('')
    
    outpath = os.path.join(BASE, "ui-config/strings.ts")
    with open(outpath, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"Generated {outpath} with {len(seen)} exports")


def generate_config_strings():
    """Rewrite config/strings.ts to use i18n messages."""
    src = os.path.join(BASE, "config/strings.ts")
    with open(src, 'r') as f:
        content = f.read()
    
    lines = []
    lines.append('/**')
    lines.append(' * App-wide API/backend strings.')
    lines.append(' * Locale is controlled by NEXT_PUBLIC_LOCALE env var.')
    lines.append(' * Translations are in i18n/messages/<locale>/messages.json')
    lines.append(' */')
    lines.append('import { UIConstants } from "@courselit/common-models";')
    lines.append('import { messages } from "../i18n";')
    lines.append('')
    lines.append('const api = messages.api;')
    lines.append('')
    
    # Extract responses object keys
    responses_match = re.search(r'export const responses = \{(.*?)\};', content, re.DOTALL)
    if responses_match:
        body = responses_match.group(1)
        
        lines.append('export const responses = {')
        
        # Extract key-value pairs
        kv_pattern = re.compile(r'(\w+)\s*:\s*((?:[^,}]|\n)*?)(?=,\s*\n|\s*\})', re.MULTILINE)
        for m in kv_pattern.finditer(body):
            key = m.group(1)
            original_value = m.group(2).strip()
            
            # Special case: mail_subject_length_exceeded uses template literal
            if key == 'mail_subject_length_exceeded':
                lines.append(f'    {key}: api.{key} ?? `Subject cannot be longer than ${{UIConstants.MAIL_SUBJECT_MAX_LENGTH}} characters`,')
            elif key == 'mail_max_recipients_exceeded':
                lines.append(f'    {key}: api.{key} ?? `Total number of recipients cannot exceed ${{UIConstants.MAIL_MAX_RECIPIENTS}}`,')
            else:
                lines.append(f'    {key}: api.{key} ?? {original_value},')
        
        lines.append('};')
        lines.append('')
    
    # Extract internal object keys
    internal_match = re.search(r'export const internal = \{(.*?)\};', content, re.DOTALL)
    if internal_match:
        body = internal_match.group(1)
        
        lines.append('export const internal = {')
        
        kv_pattern = re.compile(r'(\w+)\s*:\s*((?:[^,}]|\n)*?)(?=,\s*\n|\s*\})', re.MULTILINE)
        for m in kv_pattern.finditer(body):
            key = m.group(1)
            original_value = m.group(2).strip()
            lines.append(f'    {key}: api.{key} ?? {original_value},')
        
        lines.append('};')
        lines.append('')
    
    outpath = os.path.join(BASE, "config/strings.ts")
    with open(outpath, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"Generated {outpath}")


if __name__ == "__main__":
    generate_ui_strings()
    generate_config_strings()
